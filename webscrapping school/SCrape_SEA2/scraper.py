from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

def open_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for silent execution
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"
        
        # Open the webpage and wait for the input field to load
        page.goto(url, timeout=90000, wait_until="networkidle")
        page.wait_for_selector("#idTAUnitNo", timeout=90000)
        
        # Import the CSV file
        df = pd.read_csv("sea_combined.csv")
        
        # Define output file
        output_file = "extracted_unit_numbers.csv"
        file_exists = os.path.exists(output_file)  # Check if file already exists

        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")

        for value in df["sea_combined"].head(6):
            try:
                # Fill the input field
                text_area.fill(str(value))
                time.sleep(1)  # Small delay for stability
                
                # Click submit
                submit_button.click()
                
                # Wait for all required elements to load
                page.wait_for_selector("#__view1-__clone1", timeout=90000)
                page.wait_for_selector("#__view1-__clone3", timeout=90000)
                page.wait_for_selector("#__view1-__clone5", timeout=90000)
                page.wait_for_selector("#__view1-__clone7", timeout=90000)
                page.wait_for_selector("#__view1-__clone9", timeout=90000)
                page.wait_for_selector("#__view1-__clone11", timeout=90000)
                page.wait_for_selector("#__view3-__clone15", timeout=90000)
                page.wait_for_selector("#idUnitStatusPanel-rows-row0-col1", timeout=90000)

                # Scroll the table section upwards before extracting Manufacturer data
                scrollable_div = page.locator("#idUnitStatusPanel-sapUiTableCnt")
                for _ in range(5):  
                    scrollable_div.evaluate("(el) => el.scrollBy(0, -50)")
                    time.sleep(0.2)

                page.wait_for_selector("#idUnitStatusPanel-rows-row0-col1", timeout=5000)

                # Extract data
                unit_number = page.locator("#__view1-__clone1").text_content().strip()
                unit_type = page.locator("#__view1-__clone3").text_content().strip()
                lesse = page.locator("#__view1-__clone5").text_content().strip()
                status = page.locator("#__view1-__clone7").text_content().strip()
                city = page.locator("#__view1-__clone9").text_content().strip()
                depot = page.locator("#__view1-__clone11").text_content().strip()
                manuf_year_month = page.locator("#__view3-__clone15").text_content().strip()
                manufacturer = page.locator("#idUnitStatusPanel-rows-row0-col1").text_content().strip()

                # Print extracted data
                print(f"Processed Entry: {value}")
                print(f"Unit Number: {unit_number}, Unit Type: {unit_type}, Lesse: {lesse}, Status: {status}")
                print(f"City: {city}, Depot: {depot}, Manuf. Year/Month: {manuf_year_month}, Manufacturer: {manufacturer}")

                # Create a DataFrame for the single entry
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
                file_exists = True  # Ensure header is not written again

                print(f"Data for {value} saved.")

                # Navigate back to the input page using the back button
                back_button = page.locator("#idBackButton")
                if back_button.is_visible():
                    back_button.click()
                else:
                    page.go_back()
                
                # Wait for the input field to reappear
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                time.sleep(2)

            except Exception as e:
                print(f"Error processing entry {value}: {e}")
        
        print(f"All data saved to {output_file}")

        # Keep browser open for a few seconds before closing
        page.wait_for_timeout(5000)  # 5-second delay before closing
        
        browser.close()

if __name__ == "__main__":
    open_website()
