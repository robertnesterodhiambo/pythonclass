import threading
import pickle
from playwright.sync_api import sync_playwright
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

# Lock to avoid double saving
file_lock = threading.Lock()

# Thread-local storage for processed values
thread_local = threading.local()

# Function to load processed values from file
def load_processed_values(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return set()

# Function to save processed values to file
def save_processed_values(file_path, processed_values):
    with open(file_path, "wb") as f:
        pickle.dump(processed_values, f)

# Function to load the website page
def load_page(page, url):
    page.goto(url, timeout=400000, wait_until="domcontentloaded")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_selector("#idTAUnitNo", timeout=400000)
    print("✅ Page reloaded successfully")

# Function to perform fast scrolling
def fast_scroll(page):
    page.wait_for_selector("#idUnitStatusPanel-vsb", timeout=15000)
    page.evaluate("""
        (async function() {
            let scrollDiv = document.querySelector("#idUnitStatusPanel-vsb");
            if (scrollDiv) scrollDiv.scrollTop = 0;  // Instantly move to top
        })();
    """)

# Function to process each value
def process_entry(value, processed_values, output_file, df):
    try:
        # Check if the entry is already processed
        if value in processed_values:
            print(f"Skipping {value} (already processed)")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Set to True for silent execution
            page = browser.new_page()
            url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"
            load_page(page, url)

            text_area = page.locator("#idTAUnitNo")
            submit_button = page.locator("#idBtnUnitEnqSubmit")

            print(f"Processing {value}...")

            # Fill the input field
            text_area.fill(str(value))
            submit_button.click()

            # Wait for results
            page.wait_for_selector("#__view1-__clone1", timeout=40000)

            # Perform fast scrolling to reveal hidden content
            fast_scroll(page)

            # Extract data or mark as "Not Found"
            unit_number = page.locator("#__view1-__clone1").text_content().strip() if page.locator("#__view1-__clone1").count() > 0 else "Not Found"
            unit_type = page.locator("#__view1-__clone3").text_content().strip() if page.locator("#__view1-__clone3").count() > 0 else "Not Found"
            lesse = page.locator("#__view1-__clone5").text_content().strip() if page.locator("#__view1-__clone5").count() > 0 else "Not Found"
            status = page.locator("#__view1-__clone7").text_content().strip() if page.locator("#__view1-__clone7").count() > 0 else "Not Found"
            city = page.locator("#__view1-__clone9").text_content().strip() if page.locator("#__view1-__clone9").count() > 0 else "Not Found"
            depot = page.locator("#__view1-__clone11").text_content().strip() if page.locator("#__view1-__clone11").count() > 0 else "Not Found"
            manuf_year_month = page.locator("#__view3-__clone17").text_content().strip() if page.locator("#__view3-__clone17").count() > 0 else "Not Found"
            manufacturer = page.locator("#idUnitStatusPanel-rows-row0-col1").text_content().strip() if page.locator("#idUnitStatusPanel-rows-row0-col1").count() > 0 else "Not Found"

            # Extract On Hire Date
            on_hire_date = "Not Found"
            if page.locator("#__label55").count() > 0:
                on_hire_date = page.locator("#__label55").text_content().strip()
            elif page.locator("#idFlexBoxActivitiesBlock").count() > 0:
                on_hire_date = page.locator("#idFlexBoxActivitiesBlock").text_content().strip()

            print(f"✅ Processed Entry: {value}")

            # Create a DataFrame for the entry
            data_entry = pd.DataFrame([{
                "Input": value,
                "Unit Number": unit_number,
                "Unit Type": unit_type,
                "Lesse": lesse,
                "Status": status,
                "City": city,
                "Depot": depot,
                "Manuf. Year/Month": manuf_year_month,
                "Manufacturer": manufacturer,
                "On Hire Date": on_hire_date
            }])

            # Ensure no double saving using a lock
            with file_lock:
                data_entry.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

            # Update the processed values for this thread
            processed_values.add(value)

            browser.close()

    except Exception as e:
        print(f"⚠️ Error processing entry {value}: {e}")

# Main function to open the website
def open_website():
    df = pd.read_csv("sea_combined.csv")
    output_file = "extracted_unit_numbers.csv"
    processed_file = "processed_values.pkl"  # File to store processed entries

    # Load previously processed values
    processed_values = load_processed_values(processed_file)

    # Assign the processed values to thread-local storage
    thread_local.processed_values = processed_values

    # Using ThreadPoolExecutor to handle multiple threads
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(lambda value: process_entry(value, thread_local.processed_values, output_file, df), df["sea_combined"].astype(str))

    # Save the processed values to file after completion
    save_processed_values(processed_file, thread_local.processed_values)

    print("✅ All new data saved to output file.")

if __name__ == "__main__":
    open_website()
