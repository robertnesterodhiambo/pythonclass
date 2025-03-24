import csv
from playwright.sync_api import sync_playwright

# Input and output file names
input_csv = "combined_data.csv"
output_csv = "combined_extracted.csv"  # Updated output file name

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

# Open output CSV file for writing results
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Equipment ID", "Container Specification"])  # Write header

    # Playwright script
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
        page = browser.new_page()

        # Open the target website
        page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

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
                # Locate the 7th `<tr>` inside the table (index 6 because it starts at 0)
                container_spec = frame.locator("table tr[valign='top']").nth(5).inner_text()
                print(f"✅ Container Specification for {entry}: {container_spec}")

                # Save to CSV
                writer.writerow([entry, container_spec])

            except Exception as e:
                print(f"❌ Failed to get container specification for {entry}: {e}")
                writer.writerow([entry, "Failed to extract"])

            # Go back to enter the next entry
            page.go_back()
            page.wait_for_load_state("networkidle")

        print(f"🎉 Data saved to {output_csv}")
        browser.close()
