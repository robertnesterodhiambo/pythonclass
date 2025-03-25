from playwright.sync_api import sync_playwright
import pandas as pd
import time

def open_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run in background
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"
        page.goto(url)
        
        # Import the CSV file
        df = pd.read_csv("sea_combined.csv")
        
        # Print the first 6 entries of the 'sea_combined' column
        print(df["sea_combined"].head(6))
        
        # Insert the first 5 entries one by one into the text area with id="idTAUnitNo"
        text_area = page.locator("#idTAUnitNo")
        text_area.clear()
        for value in df["sea_combined"].head(5):
            text_area.fill(str(value))
            time.sleep(1)  # Wait for 1 second before entering the next value
        
        # Keep the browser open for interaction
        page.wait_for_timeout(10000)  # Wait for 10 seconds before closing
        
        browser.close()

if __name__ == "__main__":
    open_website()
