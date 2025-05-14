import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os
from asyncio import Semaphore
import aiofiles
import logging

# === CONFIGURATION ===
OUTPUT_FILE = "/home/dragon/DATA/extracted_unit_numbers.csv"
INPUT_FILE = "sea_combined.csv"
MAX_CONCURRENT_TASKS = 20
BATCH_SIZE = 1000
MAX_RETRIES = 3

# === LOGGING SETUP ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === UTILITIES ===
def get_processed_set():
    if os.path.exists(OUTPUT_FILE):
        try:
            processed_df = pd.read_csv(OUTPUT_FILE)
            return set(processed_df["Input"].astype(str))
        except Exception as e:
            logging.warning(f"Could not read output file: {e}")
            return set()
    return set()

def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

async def save_result(result):
    df = pd.DataFrame([result])
    file_exists = os.path.exists(OUTPUT_FILE)
    file_empty = os.path.getsize(OUTPUT_FILE) == 0 if file_exists else True
    csv_data = df.to_csv(index=False, header=file_empty)
    async with aiofiles.open(OUTPUT_FILE, mode='a') as f:
        await f.write(csv_data)

# === MAIN SCRAPER FUNCTION ===
async def extract_data(playwright, value, semaphore, retry=0):
    async with semaphore:
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"

        try:
            await page.goto(url, timeout=180000, wait_until="networkidle")
            await page.wait_for_selector("#idTAUnitNo", timeout=90000)
            await page.fill("#idTAUnitNo", value)
            await asyncio.sleep(1)
            await page.click("#idBtnUnitEnqSubmit")
            await page.wait_for_timeout(5000)

            if await page.locator("#__mbox0-cont").is_visible():
                result = {
                    "Input": value,
                    "Unit Type": "Not Found",
                    "City": "Not Found",
                    "Depot": "Not Found",
                    "Manufacturer": "Not Found"
                }
            else:
                async def get_text(locator):
                    el = page.locator(locator)
                    if await el.count() > 0 and await el.is_visible():
                        return (await el.text_content()).strip()
                    return "Not Found"

                await page.evaluate("""() => {
                    const el = document.getElementById('idUnitStatusPanel-vsb');
                    if (el) {
                        el.scrollTop = 0;
                    }
                }""")

                result = {
                    "Input": value,
                    "Unit Type": await get_text("#__view1-__clone3"),
                    "City": await get_text("#__view1-__clone9"),
                    "Depot": await get_text("#__view1-__clone11"),
                    "Manufacturer": await get_text("#idUnitStatusPanel-rows-row0-col1")
                }

            await save_result(result)
            logging.info(f"[+] Collected: {value}")

        except Exception as e:
            logging.error(f"[!] Error for {value} (attempt {retry+1}): {e}")
            if retry < MAX_RETRIES:
                await browser.close()
                await asyncio.sleep(2)
                return await extract_data(playwright, value, semaphore, retry + 1)
            else:
                result = {
                    "Input": value,
                    "Unit Type": "Error",
                    "City": "Error",
                    "Depot": "Error",
                    "Manufacturer": "Error"
                }
                await save_result(result)
                logging.warning(f"[x] Max retries reached for {value}, saved as 'Error'.")

        finally:
            await browser.close()

# === MAIN RUNNER ===
async def main():
    df = pd.read_csv(INPUT_FILE)
    df["sea_combined"] = df["sea_combined"].astype(str)

    all_entries = df["sea_combined"].tolist()
    if not all_entries:
        logging.info("❗ No entries found in input file.")
        return

    semaphore = Semaphore(MAX_CONCURRENT_TASKS)

    async with async_playwright() as playwright:
        for batch_start in range(0, len(all_entries), BATCH_SIZE):
            # Refresh processed set before each batch
            processed_set = get_processed_set()

            batch_entries = [
                entry for entry in all_entries[batch_start:batch_start + BATCH_SIZE]
                if entry not in processed_set
            ]

            if not batch_entries:
                logging.info("✅ All entries in this batch already processed. Skipping.")
                continue

            logging.info(f"🚀 Starting batch with {len(batch_entries)} entries...")
            tasks = [extract_data(playwright, entry, semaphore) for entry in batch_entries]
            await asyncio.gather(*tasks, return_exceptions=True)
            logging.info(f"✅ Finished batch of {len(batch_entries)} entries.")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
