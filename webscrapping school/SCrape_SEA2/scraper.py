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
            page.goto(url, timeout=90000, wait_until="networkidle")
            page.wait_for_selector("#idTAUnitNo", timeout=90000)
            print("✅ Page reloaded successfully")

        # Load page initially
        load_page()

        # Import the CSV file containing input values
        df = pd.read_csv("sea_combined.csv")

        # Define output file
        output_file = "extracted_unit_numbers.csv"
        file_exists = os.path.exists(output_file)

        # Load existing data if file exists
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
                print(f"Skipping {value} (already processed)")
                continue

            if new_entries_count >= 5:
                print("✅ Collected 5 new entries, stopping execution.")
                break  

            try:
                # Fill the input field
                text_area.fill(str(value))
                time.sleep(1)

                # Click submit
                submit_button.click()

                # Wait for results
                page.wait_for_selector("#__view1-__clone1", timeout=90000)
                time.sleep(5)  

                # Check if "No Data Found" message appears
                if page.locator("#noDataMessage").is_visible():
                    print(f"⚠️ No data found for {value}. Saving as 'Not Found'.")
                    data_entry = pd.DataFrame([{
                        "Input": value,
                        "Unit Number": "Not Found",
                        "Unit Type": "Not Found",
                        "Lesse": "Not Found",
                        "Status": "Not Found",
                        "City": "Not Found",
                        "Depot": "Not Found",
                        "Manuf. Year/Month": "Not Found",
                        "Manufacturer": "Not Found"
                    }])
                else:
                    # Extract data if found
                    unit_number = page.locator("#__view1-__clone1").text_content().strip()
                    unit_type = page.locator("#__view1-__clone3").text_content().strip()
                    lesse = page.locator("#__view1-__clone5").text_content().strip()
                    status = page.locator("#__view1-__clone7").text_content().strip()
                    city = page.locator("#__view1-__clone9").text_content().strip()
                    depot = page.locator("#__view1-__clone11").text_content().strip()
                    manuf_year_month = page.locator("#__view3-__clone17").text_content().strip()
                    manufacturer = page.locator("#idUnitStatusPanel-rows-row0-col1").text_content().strip()

                    print(f"✅ Processed Entry: {value}")
                    print(f"Unit Number: {unit_number}, Unit Type: {unit_type}, Lesse: {lesse}, Status: {status}")

                    # Create a DataFrame for the entry
                    data_entry = pd.DataFrame([{
                        "Input": value,
                        "Unit Number": unit_number,
                        "Unit Type": unit_type,
                        "Lesse": lesse,
                        "Status": status,
                        "City": city,
                        "Depot": depot,
                        "Manuf. Year/Month": manuf_year_month,
                        "Manufacturer": manufacturer
                    }])

                # Append data to CSV immediately
                data_entry.to_csv(output_file, mode='a', header=not file_exists, index=False)
                file_exists = True  

                print(f"✅ Data for {value} saved.")
                new_entries_count += 1  

            except Exception as e:
                print(f"⚠️ Timeout/Error processing entry {value}: {e}")
                print("🚨 Saving as 'Timeout' and moving to next entry.")

                # Save "Timeout" entry
                timeout_entry = pd.DataFrame([{
                    "Input": value,
                    "Unit Number": "Timeout",
                    "Unit Type": "Timeout",
                    "Lesse": "Timeout",
                    "Status": "Timeout",
                    "City": "Timeout",
                    "Depot": "Timeout",
                    "Manuf. Year/Month": "Timeout",
                    "Manufacturer": "Timeout"
                }])
                timeout_entry.to_csv(output_file, mode='a', header=not file_exists, index=False)
                file_exists = True  

            # Reopen the URL for the next entry
            load_page()

        print(f"✅ All new data saved to {output_file}")
        page.wait_for_timeout(5000)  
        browser.close()

if __name__ == "__main__":
    open_website()
