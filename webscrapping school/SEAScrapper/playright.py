import csv
from playwright.sync_api import sync_playwright

# Load CSV file and get first 5 entries
csv_file = "combined_data.csv"  # Ensure this file is in the same folder as the script
entries = []

with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        if row:  # Ensure the row is not empty
            entries.append(row[0])  # Get first column value
        if len(entries) == 5:  # Stop after 5 entries
            break

# Playwright script to enter data into text area
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True to run in the background
    page = browser.new_page()

    # Open the target website
    page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

    for entry in entries:
        print(f"Entering: {entry}")
        page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  # Fill text area
        page.wait_for_timeout(1000)  # Small delay (optional)

    input("Press Enter to close...")  # Keeps the browser open for inspection
    browser.close()
