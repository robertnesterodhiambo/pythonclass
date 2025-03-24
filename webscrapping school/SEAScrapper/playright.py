import csv
import time
from bs4 import BeautifulSoup
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
    writer.writerow(["Equipment ID", "Factory Name", "Manufacture Date & Model", "Current Status", "Move Date", "Location", "Lease Code", "Customer Name"])  # Updated columns

    # Playwright script
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True for background execution
        page = browser.new_page()

        # Open the target website
        page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx")

        for entry in entries:
            print(f"🔹 Entering: {entry}")

            attempts = 2  # Number of retry attempts

            while attempts > 0:
                try:
                    # Fill the text area
                    page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  

                    # Click the "Preview" button
                    page.locator("input.btn_tex_basic", has_text="Preview").click()

                    # Wait for the frame to load
                    page.wait_for_timeout(3000)

                    # Select the frame by ID (id="report")
                    frame = page.frame("report")

                    # Get the full page content using BeautifulSoup
                    soup = BeautifulSoup(frame.content(), "html.parser")

                    # Extract data using BeautifulSoup
                    def get_text_by_class(class_names):
                        """Finds the first available text from a list of class names."""
                        for class_name in class_names:
                            element = soup.find("td", class_=class_name)
                            if element:
                                return element.text.strip()
                        return "Not Found"

                    factory_name = get_text_by_class(["a115cl"])
                    manufacture_date_model = get_text_by_class(["a123cl"])
                    current_status = get_text_by_class(["a500"])
                    move_date = get_text_by_class(["a504"])

                    # Extract Location from multiple possible classes
                    location = get_text_by_class(["a520", "a520cl r14"])

                    # Extract Lease Code from multiple possible classes
                    lease_code = get_text_by_class(["a512", "a512c r14", "a512c"])

                    # Extract Customer Name from multiple possible classes
                    customer_name = get_text_by_class(["a516", "a516c r14"])

                    print(f"✅ Extracted: Factory Name: {factory_name}, Manufacture Date & Model: {manufacture_date_model}, Current Status: {current_status}, Move Date: {move_date}, Location: {location}, Lease Code: {lease_code}, Customer Name: {customer_name}")

                    # Write to CSV immediately (prevents memory issues)
                    writer.writerow([entry, factory_name, manufacture_date_model, current_status, move_date, location, lease_code, customer_name])

                    # Clear page content to free memory
                    page.evaluate("document.body.innerHTML = ''")

                    break  # Exit loop on success

                except Exception as e:
                    print(f"❌ Error extracting data for {entry}: {e}")

                    attempts -= 1  # Reduce retry count

                    if attempts > 0:
                        print(f"🔄 Reloading page and retrying for {entry}...")
                        page.reload()
                        time.sleep(2)  # Small delay before retrying
                    else:
                        print(f"🚨 Final failure for {entry}, skipping...")
                        writer.writerow([entry, "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract"])

            # Go back to enter the next entry
            page.go_back()
            page.wait_for_load_state("networkidle")

            # Small delay to prevent CPU overload
            time.sleep(1)

        print(f"🎉 Data saved to {output_csv}")
        browser.close()
