from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import threading

def process_entries(entries, output_file, thread_id):
    lock = threading.Lock()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"

        def load_page():
            try:
                page.goto(url, timeout=90000, wait_until="networkidle")
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                print(f"✅ [Thread {thread_id}] Page loaded successfully")
            except Exception as e:
                print(f"⚠️ [Thread {thread_id}] Error loading page: {e}. Retrying...")
                time.sleep(5)
                page.reload()
                page.wait_for_selector("#idTAUnitNo", timeout=90000)

        def scroll_table():
            try:
                page.wait_for_selector("#idUnitStatusPanel-vsb", timeout=15000)
                page.evaluate("""
                    (async function() {
                        let scrollDiv = document.querySelector("#idUnitStatusPanel-vsb");
                        if (!scrollDiv) return;

                        let lastScroll = -1;
                        while (scrollDiv.scrollTop !== lastScroll) {
                            lastScroll = scrollDiv.scrollTop;
                            scrollDiv.scrollBy(0, -200);
                            await new Promise(r => setTimeout(r, 500));
                        }
                    })();
                """)
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"⚠️ [Thread {thread_id}] Error while scrolling: {e}")

        def get_text(locator):
            try:
                element = page.locator(locator)
                if element.is_visible():
                    return element.text_content().strip()
                return "Not Found"
            except Exception:
                return "Not Found"

        load_page()
        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")

        for value in entries:
            try:
                text_area.fill(str(value))
                time.sleep(1)
                submit_button.click()
                page.wait_for_timeout(5000)

                # Check for "No Data" popup
                if page.locator("#__mbox0-cont").is_visible():
                    print(f"⚠️ [Thread {thread_id}] No data for {value}, logging as Not Found and reloading.")
                    data_entry = pd.DataFrame([{
                        "Input": value, "Unit Number": "Not Found", "Unit Type": "Not Found",
                        "Lesse": "Not Found", "Status": "Not Found", "City": "Not Found", 
                        "Depot": "Not Found", "Manuf. Year/Month": "Not Found", "Manufacturer": "Not Found", 
                        "On Hire Date": "Not Found"
                    }])
                    with lock:
                        data_entry.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                    page.reload()
                    page.wait_for_selector("#idTAUnitNo", timeout=60000)
                    continue

                page.wait_for_selector("#__view1-__clone1", timeout=10000)
                scroll_table()

                # Extract On Hire Date
                on_hire_date = "Not Found"
                if page.locator("#__label55").count() > 0:
                    on_hire_date = page.locator("#__label55").text_content().strip()
                elif page.locator("#idFlexBoxActivitiesBlock").count() > 0:
                    on_hire_date = page.locator("#idFlexBoxActivitiesBlock").text_content().strip()

                if page.locator("#noDataMessage").is_visible():
                    data_entry = pd.DataFrame([{ 
                        "Input": value, "Unit Number": "Not Found", "Unit Type": "Not Found",
                        "Lesse": "Not Found", "Status": "Not Found", "City": "Not Found", 
                        "Depot": "Not Found", "Manuf. Year/Month": "Not Found", "Manufacturer": "Not Found", 
                        "On Hire Date": on_hire_date
                    }])
                else:
                    data_entry = pd.DataFrame([{ 
                        "Input": value, 
                        "Unit Number": get_text("#__view1-__clone1"),
                        "Unit Type": get_text("#__view1-__clone3"),
                        "Lesse": get_text("#__view1-__clone5"),
                        "Status": get_text("#__view1-__clone7"),
                        "City": get_text("#__view1-__clone9"),
                        "Depot": get_text("#__view1-__clone11"),
                        "Manuf. Year/Month": get_text("#__view3-__clone17"),
                        "Manufacturer": get_text("#idUnitStatusPanel-rows-row0-col1"),
                        "On Hire Date": on_hire_date
                    }])

                with lock:
                    data_entry.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                print(f"✅ [Thread {thread_id}] Processed {value}")

            except Exception as e:
                print(f"⚠️ [Thread {thread_id}] Error processing {value}: {e}")
                load_page()
                continue

        browser.close()
        print(f"✅ [Thread {thread_id}] Completed processing.")

if __name__ == "__main__":
    while True:
        df = pd.read_csv("sea_combined.csv")
        #df = pd.read_csv(r"C:\Users\Dragon\Documents\sea_combined.csv")
        output_file = "extracted_unit_numbers.csv"
        existing_entries = set()

        if os.path.exists(output_file):
            existing_data = pd.read_csv(output_file)
            existing_entries = set(existing_data["Input"].astype(str))

        new_entries = []
        for val in df["sea_combined"].astype(str):
            if val in existing_entries:
                print(f"⏩ Skipping already processed entry: {val}")
            else:
                new_entries.append(val)

        if not new_entries:
            print("✅ No new entries to process. Exiting.")
            break

        batch_size = 224
        total_entries = len(new_entries)

        for batch_start in range(0, total_entries, batch_size):
            batch_entries = new_entries[batch_start:batch_start + batch_size]

            chunk_size = len(batch_entries) // 30
            threads = []

            for i in range(30):
                start_idx = i * chunk_size
                end_idx = None if i == 29 else (i + 1) * chunk_size
                thread = threading.Thread(target=process_entries, args=(batch_entries[start_idx:end_idx], output_file, i + 1))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"✅ Processed {len(batch_entries)} entries. Restarting to free memory...")
            time.sleep(10)