from playwright.sync_api import sync_playwright
import pandas as pd
import time

def open_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run in background
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"
        
        # Wait until network activity is idle
        page.goto(url, timeout=90000, wait_until="networkidle")
        
        # Ensure the input field is available before proceeding
        page.wait_for_selector("#idTAUnitNo", timeout=90000)
        
        # Import the CSV file
        df = pd.read_csv("sea_combined.csv")
        
        # Print the first 6 entries of the 'sea_combined' column
        print(df["sea_combined"].head(6))
        
        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")
        back_button = "#idBackButton"  # Adjust this if the actual ID is different
        
        for value in df["sea_combined"].head(6):
            text_area.fill(str(value))
            time.sleep(1)  # Wait for 1 second before submitting
            
            submit_button.click()
            
            # Wait for the result page to fully load by checking the presence of span with id "__view1-__clone1"
            page.wait_for_selector("#__view1-__clone1", timeout=90000)
            time.sleep(2)
            
            # Process the result here if needed
            print(f"Processed entry: {value}")
            
            # Go back to the input page
            page.go_back()
            
            # Wait for the input field to reappear before proceeding
            page.wait_for_selector("#idTAUnitNo", timeout=90000)
            time.sleep(2)
        
        # Keep the browser open for interaction
        page.wait_for_timeout(10000)  # Wait for 10 seconds before closing
        
        browser.close()

if __name__ == "__main__":
    open_website()
