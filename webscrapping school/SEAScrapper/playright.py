import csv
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Input and output file names
input_csv = "combined_data.csv"
output_csv = "combined_extracted.csv"  # Output file name

# Load CSV file and get first 5 entries
entries = []

with open(input_csv, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        if row:
            entries.append(row[0])  # Get the first column value
        if len(entries) == 5:  # Process only the first 5 entries
            break

# Playwright script
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
    page = browser.new_page()

    # Open the target website
    page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

    extracted_data = []  # Store extracted factory names

    for entry in entries:
        print(f"🔹 Entering: {entry}")

        # Fill the text area
        page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  

        # Click the "Preview" button
        page.locator("input.btn_tex_basic", has_text="Preview").click()

        # Wait for the frame to load
        page.wait_for_timeout(3000)

        # Select the frame by ID (id="report")
        frame = page.frame("report")

        try:
            # Extract all HTML inside the iframe
            html_content = frame.locator("body").inner_html()

            # Use BeautifulSoup to parse the HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # Find the first <td> with class "a115cl"
            factory_name_td = soup.find("td", class_="a115cl")

            # Extract text or mark as "Not Found"
            factory_name = factory_name_td.get_text(strip=True) if factory_name_td else "Not Found"

            print(f"✅ Factory Name for {entry}: {factory_name}")

            # Save to list
            extracted_data.append([entry, factory_name])

        except Exception as e:
            print(f"❌ Failed to extract Factory Name for {entry}: {e}")
            extracted_data.append([entry, "Failed to extract"])

        # Go back to enter the next entry
        page.go_back()
        page.wait_for_load_state("networkidle")

    # Save extracted structured data into CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Equipment ID", "Factory Name"])  # Updated column name
        writer.writerows(extracted_data)

    print(f"🎉 Data saved to {output_csv}")
    browser.close()
