import csv
import time
from playwright.sync_api import sync_playwright

# Input and output file names
input_csv = "combined_data.csv"
output_csv = "combined_extracted.csv"  # Output file name

# Load CSV file and get first 5 entries
entries = []

with open(input_csv, newline='', encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        if row:
            entries.append(row[0])  # Get the first column value
        if len(entries) == 5:  # Process only the first 5 entries
            break

# Open output CSV file and write headers
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Equipment ID", "Factory Name", "Manufacture Date & Model"])  # Updated column names

    # Playwright script
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
        page = browser.new_page()

        # Open the target website
        page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

        for entry in entries:
            print(f"🔹 Entering: {entry}")

            try:
                # Fill the text area
                page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  

                # Click the "Preview" button
                page.locator("input.btn_tex_basic", has_text="Preview").click()

                # Wait for the frame to load
                page.wait_for_timeout(3000)

                # Select the frame by ID (id="report")
                frame = page.frame("report")

                # Extract Factory Name from <td class="a115cl">
                factory_name = frame.locator("td.a115cl").first.inner_text(timeout=2000)

                # Extract Manufacture Date & Model from <td class="a123cl">
                manufacture_date_model = frame.locator("td.a123cl").first.inner_text(timeout=2000)

                print(f"✅ Factory Name: {factory_name}, Manufacture Date & Model: {manufacture_date_model}")

                # Write to CSV immediately (prevents memory issues)
                writer.writerow([entry, factory_name, manufacture_date_model])

            except Exception as e:
                print(f"❌ Failed to extract data for {entry}: {e}")
                writer.writerow([entry, "Failed to extract", "Failed to extract"])

            # Go back to enter the next entry
            page.go_back()
            page.wait_for_load_state("networkidle")

            # Small delay to prevent CPU overload
            time.sleep(1)

        print(f"🎉 Data saved to {output_csv}")
        browser.close()
