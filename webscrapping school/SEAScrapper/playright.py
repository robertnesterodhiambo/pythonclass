import csv
import time
import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Input and output file names
input_csv = "combined_data.csv"
output_csv = "combined_extracted.csv"

# Load already processed equipment IDs from output file
processed_ids = set()
if os.path.exists(output_csv):
    with open(output_csv, newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if row:
                processed_ids.add(row[0])  # Store processed Equipment IDs

# Load only the first 131,279 entries from the input CSV (as per your request)
entries_to_check = []
with open(input_csv, newline='', encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header if present
    for row in reader:
        if row:
            entries_to_check.append(row[0])  # Get the first column value
        if len(entries_to_check) == 131279:  # Keep the original limit
            break

# Find IDs that are missing in the processed file
missing_entries = [entry for entry in entries_to_check if entry not in processed_ids]

# If all entries are already processed, exit the script
if not missing_entries:
    print("✅ All first 131,279 equipment IDs have already been processed. No new searches needed.")
    exit()

# Ensure the CSV file has a header before appending
if not os.path.exists(output_csv) or os.stat(output_csv).st_size == 0:
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Equipment ID", "Factory Name", "Manufacture Date & Model", "Current Status", "Move Date", "Location", "Lease Code", "Customer Name"])

# Function to open website with retry mechanism
def open_website_with_retry(page, max_retries=3):
    """Tries to load the website up to max_retries times if it fails."""
    retries = 0
    while retries < max_retries:
        try:
            print(f"🌐 Loading website (Attempt {retries + 1}/{max_retries})...")
            page.goto("https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx", timeout=60000)
            return True
        except Exception as e:
            print(f"❌ Failed to load website: {e}")
            retries += 1
            time.sleep(5)  # Wait before retrying
    print("🚨 Final failure loading website, exiting...")
    exit()  # Exit script if website never loads

# Start Playwright session
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set headless=True for background execution
    page = browser.new_page()

    # Open the target website
    open_website_with_retry(page)

    search_count = 0  # Track number of searches

    for entry in missing_entries:
        print(f"🔹 Checking: {entry}")

        attempts = 2  # Number of retry attempts

        while attempts > 0:
            try:
                # Fill the text area
                page.fill("#ctl00_bodyContent_ucEqpIds_txtEqpId", entry)  

                # Click the "Preview" button
                page.locator("input.btn_tex_basic", has_text="Preview").click()

                # Wait for the frame to load
                page.wait_for_load_state("load", timeout=60000)  # Avoids networkidle timeout issues

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

                # Prepare the extracted data
                extracted_data = [entry, factory_name, manufacture_date_model, current_status, move_date, location, lease_code, customer_name]

                print(f"✅ Data saved: {extracted_data}")

                # Save the extracted data immediately before moving to the next entry
                with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(extracted_data)

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
                    failed_data = [entry, "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract", "Failed to extract"]
                    
                    # Save failed attempt
                    with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(failed_data)
                    
                    print(f"❌ Data saved: {failed_data}")

        # Go back to enter the next entry
        page.go_back()
        page.wait_for_load_state("load", timeout=60000)

        # Small delay to prevent CPU overload
        time.sleep(1)

        # Increment search count
        search_count += 1

        # Restart Playwright every 20 searches to prevent crashes
        if search_count % 20 == 0:
            print("🔄 Restarting browser to prevent memory leaks...")
            browser.close()
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            open_website_with_retry(page)  # Ensure the website loads after restart

    print(f"🎉 Data saved to {output_csv}")
    browser.close()
