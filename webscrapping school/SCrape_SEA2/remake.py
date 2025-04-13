from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os
import threading

def process_entries(entries, output_file, thread_id):
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
                return ""
            except Exception:
                return ""

        load_page()

        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")
        
        for value in entries:
            try:
                text_area.fill(str(value))
                time.sleep(1)
                submit_button.click()
                page.wait_for_selector("#__view1-__clone1", timeout=10000)
                scroll_table()

                # Prepare the dictionary to save results
                data_entry = {
                    "Input": value,
                    "Unit Number": "", "Unit Type": "", "Lesse": "", "Status": "", 
                    "City": "", "Depot": "", "Manuf. Year/Month": "", "Manufacturer": "", "On Hire Date": ""
                }

                # Check if the popup appears
                if page.locator("#__mbox0-hdr").is_visible():
                    print(f"⚠️ [Thread {thread_id}] Popup detected. Storing searched number for {value}")
                    data_entry["Unit Number"] = "Popup detected"
                    # Write the data_entry even if the popup appears
                    with threading.Lock():
                        pd.DataFrame([data_entry]).to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                    page.reload()  # Refresh the page after popup detection
                    time.sleep(5)
                    continue  # Skip further processing for this entry

                # Extract On Hire Date
                on_hire_date = ""
                if page.locator("#__label55").count() > 0:
                    on_hire_date = page.locator("#__label55").text_content().strip()
                elif page.locator("#idFlexBoxActivitiesBlock").count() > 0:
                    on_hire_date = page.locator("#idFlexBoxActivitiesBlock").text_content().strip()

                # If there's no data (no results), write the input value with blank fields
                if page.locator("#noDataMessage").is_visible():
                    data_entry["On Hire Date"] = on_hire_date
                    with threading.Lock():
                        pd.DataFrame([data_entry]).to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                    continue

                # Otherwise, extract the actual data
                data_entry["Unit Number"] = get_text("#__view1-__clone1")
                data_entry["Unit Type"] = get_text("#__view1-__clone3")
                data_entry["Lesse"] = get_text("#__view1-__clone5")
                data_entry["Status"] = get_text("#__view1-__clone7")
                data_entry["City"] = get_text("#__view1-__clone9")
                data_entry["Depot"] = get_text("#__view1-__clone11")
                data_entry["Manuf. Year/Month"] = get_text("#__view3-__clone17")
                data_entry["Manufacturer"] = get_text("#idUnitStatusPanel-rows-row0-col1")
                data_entry["On Hire Date"] = on_hire_date

                # Save the result, even if there was no data found or if timeout occurred
                with threading.Lock():
                    pd.DataFrame([data_entry]).to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                print(f"✅ [Thread {thread_id}] Processed {value}")
            
            except Exception as e:
                print(f"⚠️ [Thread {thread_id}] Error processing {value}: {e}")
                # Write the input value even if there's an error or timeout
                data_entry = { "Input": value, "Unit Number": "Error", "Unit Type": "", "Lesse": "", "Status": "", 
                               "City": "", "Depot": "", "Manuf. Year/Month": "", "Manufacturer": "", "On Hire Date": "" }
                with threading.Lock():
                    pd.DataFrame([data_entry]).to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                continue

        browser.close()
        print(f"✅ [Thread {thread_id}] Completed processing.")

if __name__ == "__main__":
    while True:
        df = pd.read_csv("sea_combined.csv")
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

        batch_size = 100  # Process 100 entries at a time
        total_entries = len(new_entries)

        for batch_start in range(0, total_entries, batch_size):
            batch_entries = new_entries[batch_start:batch_start + batch_size]

            chunk_size = len(batch_entries) // 10  # Now using 6 browsers
            threads = []

            for i in range(10):  # Launch 6 threads
                start_idx = i * chunk_size
                end_idx = None if i == 5 else (i + 1) * chunk_size
                thread = threading.Thread(target=process_entries, args=(batch_entries[start_idx:end_idx], output_file, i + 1))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            print(f"✅ Processed {len(batch_entries)} entries. Restarting to free memory...")
            time.sleep(10)  # Allow some cooldown before restarting
