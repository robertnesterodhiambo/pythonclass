from playwright.sync_api import sync_playwright
import pandas as pd
import time

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
        
        # List to store extracted data
        extracted_data = []

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
                
                # Store in the list
                extracted_data.append({
                    "Input": value,
                    "Unit Number": unit_number,
                    "Unit Type": unit_type,
                    "Lesse": lesse,
                    "Status": status,
                    "City": city,
                    "Depot": depot,
                    "Manuf. Year/Month": manuf_year_month,
                    "Manufacturer": manufacturer
                })

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
        
        # Convert extracted data into a DataFrame
        result_df = pd.DataFrame(extracted_data)
        
        # Save to CSV
        result_df.to_csv("extracted_unit_numbers.csv", index=False)
        print("Data saved to extracted_unit_numbers.csv")
        
        # Keep browser open for a few seconds before closing
        page.wait_for_timeout(5000)  # 5-second delay before closing
        
        browser.close()

if __name__ == "__main__":
    open_website()
