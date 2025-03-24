import csv
from playwright.sync_api import sync_playwright

# Load CSV file and get first 5 entries
csv_file = "combined_data.csv"  # Ensure this file is in the same folder as the script
entries = []

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        if row:  # Ensure row is not empty
            entries.append(row[0])  # Get first column value
        if len(entries) == 5:  # Stop after 5 entries
            break

# Playwright script to enter data and click "Preview"
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
    page = browser.new_page()

    # Open the target website
    page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

    for entry in entries:
        print(f"Entering: {entry}")
        
        # Fill the text area
        page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  
        
        # Click the "Preview" button
        page.locator("input.btn_tex_basic", has_text="Preview").click()
        
        # Wait for the page to load (adjust if needed)
        page.wait_for_load_state("networkidle")
        
        # Wait for 2 seconds to allow preview (Adjust as needed)
        page.wait_for_timeout(2000)  
        
        # Go back to the previous page
        page.go_back()
        
        # Wait for page reload
        page.wait_for_load_state("networkidle")
        
    print("✅ Completed entering 5 entries!")
    browser.close()
