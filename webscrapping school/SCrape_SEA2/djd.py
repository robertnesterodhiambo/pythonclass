from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

def open_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for silent execution
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"

        def load_page():
            """Reopen the page and wait for it to fully load"""
            try:
                page.goto(url, timeout=90000, wait_until="networkidle")
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                print("✅ Page reloaded successfully")
            except Exception as e:
                print(f"⚠️ Error loading page: {e}. Retrying...")
                time.sleep(5)
                page.reload()
                page.wait_for_selector("#idTAUnitNo", timeout=90000)

        def scroll_table():
            """Scrolls the table up to reveal hidden content"""
            try:
                page.wait_for_selector("#idUnitStatusPanel-vsb", timeout=15000)
                page.evaluate("""
                    (async function() {
                        let scrollDiv = document.querySelector("#idUnitStatusPanel-vsb");
                        if (!scrollDiv) return;
                        
                        let lastScroll = -1;
                        while (scrollDiv.scrollTop !== lastScroll) {
                            lastScroll = scrollDiv.scrollTop;
                            scrollDiv.scrollBy(0, -200);  // Scroll UP by 200 pixels
                            await new Promise(r => setTimeout(r, 500)); // Wait for content to load
                        }
                    })();
                """)
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"⚠️ Error while scrolling: {e}")

        def get_text(locator):
            """Returns text content of an element if found, else 'Not Found'"""
            try:
                element = page.locator(locator)
                if element.is_visible():
                    return element.text_content().strip()
                return "Not Found"
            except Exception:
                return "Not Found"

        # Load the page initially
        load_page()

        df = pd.read_csv("sea_combined.csv")
        output_file = "extracted_unit_numbers.csv"
        file_exists = os.path.exists(output_file)

        if file_exists:
            existing_data = pd.read_csv(output_file)
            processed_values = set(existing_data["Input"].astype(str))
        else:
            processed_values = set()

        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")
        new_entries_count = 0

        for value in df["sea_combined"].astype(str):
            if value in processed_values:
                print(f"⏩ Skipping {value} (already processed)")
                continue

            if new_entries_count >= 312640:
                print("✅ Collected required entries, stopping execution.")
                break  

            try:
                text_area.fill(str(value))
                time.sleep(1)
                submit_button.click()
                page.wait_for_selector("#__view1-__clone1", timeout=10000)
                scroll_table()

                if page.locator("#noDataMessage").is_visible():
                    print(f"⚠️ No data found for {value}. Saving as 'Not Found'.")
                    data_entry = pd.DataFrame([{ 
                        "Input": value, "Unit Number": "Not Found", "Unit Type": "Not Found",
                        "Lesse": "Not Found", "Status": "Not Found", "City": "Not Found", 
                        "Depot": "Not Found", "Manuf. Year/Month": "Not Found", "Manufacturer": "Not Found" 
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
                        "Manufacturer": get_text("#idUnitStatusPanel-rows-row0-col1")
                    }])

                    print(f"✅ Processed Entry: {value}")
                    print(f"🔹 Unit Number: {data_entry.iloc[0]['Unit Number']}, Type: {data_entry.iloc[0]['Unit Type']}, Status: {data_entry.iloc[0]['Status']}")

                try:
                    data_entry.to_csv(output_file, mode='a', header=not file_exists, index=False)
                    file_exists = True  
                    print(f"✅ Data for {value} saved successfully.")
                    new_entries_count += 1  
                except Exception as e:
                    print(f"⚠️ Error saving data: {e}")

            except Exception as e:
                print(f"⚠️ Error processing entry {value}: {e}. Refreshing page and moving to next entry.")
                load_page()  # Refresh the website before continuing to the next entry
                continue  # Skip to the next iteration

            load_page()
        
        print(f"✅ All new data saved to {output_file}")
        page.wait_for_timeout(5000)  
        browser.close()

if __name__ == "__main__":
    open_website()
