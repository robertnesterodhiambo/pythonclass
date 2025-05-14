# Full Modified Code with Asyncio, Targeted Fields, and Optimizations

import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import os
from asyncio import Semaphore
import aiofiles

OUTPUT_FILE = "/home/dragon/DATA/extracted_unit_numbers.csv"
INPUT_FILE = "sea_combined.csv"
MAX_CONCURRENT_TASKS = 10
BATCH_SIZE = 1000

def get_processed_set():
    if os.path.exists(OUTPUT_FILE):
        processed_df = pd.read_csv(OUTPUT_FILE)
        return set(processed_df["Input"].astype(str))
    return set()

def chunk_list(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

async def extract_data(playwright, value, semaphore):
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

            # Check if no data message is shown
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

                result = {
                    "Input": value,
                    "Unit Type": await get_text("#__view1-__clone3"),
                    "City": await get_text("#__view1-__clone9"),
                    "Depot": await get_text("#__view1-__clone11"),
                    "Manufacturer": await get_text("#idUnitStatusPanel-rows-row0-col1")
                }
        except Exception as e:
            print(f"[!] Error for {value}: {e}")
            result = {
                "Input": value,
                "Unit Type": "Not Found",
                "City": "Not Found",
                "Depot": "Not Found",
                "Manufacturer": "Not Found"
            }
        finally:
            await browser.close()

        # Append to CSV
        async with aiofiles.open(OUTPUT_FILE, mode='a') as f:
            df = pd.DataFrame([result])
            write_header = not os.path.exists(OUTPUT_FILE)
            await f.write(df.to_csv(index=False, header=write_header if os.path.getsize(OUTPUT_FILE) == 0 else False))
        print(f"[+] Collected {value}")

async def main():
    df = pd.read_csv(INPUT_FILE)
    df["sea_combined"] = df["sea_combined"].astype(str)

    processed_set = get_processed_set()
    unprocessed_df = df[~df["sea_combined"].isin(processed_set)]

    new_entries = unprocessed_df["sea_combined"].tolist()
    if not new_entries:
        print("✅ No new entries to process. Exiting.")
        return

    semaphore = Semaphore(MAX_CONCURRENT_TASKS)

    async with async_playwright() as playwright:
        for batch in chunk_list(new_entries, BATCH_SIZE):
            print(f"🚀 Starting batch of {len(batch)} entries...")
            tasks = [extract_data(playwright, entry, semaphore) for entry in batch]
            await asyncio.gather(*tasks)
            print(f"✅ Finished batch of {len(batch)} entries.")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
