from playwright.sync_api import sync_playwright
import pandas as pd
import os
import re

def open_website():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for silent execution
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"

        def load_page():
            """Reopen the page and wait for it to fully load"""
            page.goto(url, timeout=400000, wait_until="domcontentloaded")  
            page.wait_for_load_state("domcontentloaded")  
            page.wait_for_selector("#idTAUnitNo", timeout=400000)
            print("✅ Page reloaded successfully")

        def fast_scroll():
            """Quickly scrolls to reveal hidden content"""
            page.wait_for_selector("#idUnitStatusPanel-vsb", timeout=15000)
            page.evaluate("""
                (async function() {
                    let scrollDiv = document.querySelector("#idUnitStatusPanel-vsb");
                    if (scrollDiv) scrollDiv.scrollTop = 0;  // Instantly move to top
                })();
            """)

        # Load page initially
        load_page()

        # Import the CSV file containing input values
        df = pd.read_csv("sea_combined.csv")

        # Define output file
        output_file = "extracted_unit_numbers.csv"
        file_exists = os.path.exists(output_file)

        # Load existing data if file exists
        if file_exists:
            existing_data = pd.read_csv(output_file)
            processed_values = set(existing_data["Input"].astype(str))
        else:
            processed_values = set()

        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")

        new_entries_count = 0

        for value in df["sea_combined"].astype(str):
            if value in processed_values:
                print(f"Skipping {value} (already processed)")
                continue

            if new_entries_count >= 312640:
                print("✅ Collected 5 new entries, stopping execution.")
                break  

            try:
                # Fill the input field
                text_area.fill(str(value))

                # Click submit
                submit_button.click()

                # Wait for results
                page.wait_for_selector("#__view1-__clone1", timeout=40000)

                # Perform fast scrolling to reveal hidden content
                fast_scroll()

                # If "No Data Found" appears, save immediately
                if page.locator("#noDataMessage").count() > 0:
                    print(f"⚠️ No data found for {value}. Saving as 'Not Found'.")
                    data_entry = pd.DataFrame([{
                        "Input": value,
                        "Unit Number": "Not Found",
                        "Unit Type": "Not Found",
                        "Lesse": "Not Found",
                        "Status": "Not Found",
                        "City": "Not Found",
                        "Depot": "Not Found",
                        "Manuf. Year/Month": "Not Found",
                        "Manufacturer": "Not Found",
                        "On Hire Date": "Not Found"
                    }])
                else:
                    # Extract information
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

                # Append data to CSV immediately
                data_entry.to_csv(output_file, mode='a', header=not file_exists, index=False)
                file_exists = True  
                print(f"✅ Data for {value} saved.")
                new_entries_count += 1  

            except Exception as e:
                print(f"⚠️ Timeout/Error processing entry {value}: {e}")
                
            # Reopen the URL for the next entry
            load_page()

        print(f"✅ All new data saved to {output_file}")
        browser.close()

if __name__ == "__main__":
    open_website()