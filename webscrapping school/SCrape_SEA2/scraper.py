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
                
                # Wait for the result page to load
                page.wait_for_selector("#__view1-__clone1", timeout=90000)
                page.wait_for_selector("#__view1-__clone3", timeout=90000)
                
                # Extract data
                unit_number = page.locator("#__view1-__clone1").text_content().strip()
                unit_type = page.locator("#__view1-__clone3").text_content().strip()
                
                # Print extracted data
                print(f"Processed Entry: {value}, Unit Number: {unit_number}, Unit Type: {unit_type}")
                
                # Store in the list
                extracted_data.append({
                    "Input": value,
                    "Unit Number": unit_number,
                    "Unit Type": unit_type
                })

                # Go back to the input page
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
