from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

def process_entries(entries, output_file):
    collected = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        url = "https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html"

        def load_page():
            try:
                page.goto(url, timeout=180000, wait_until="networkidle")
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                print("Page loaded successfully")
            except Exception as e:
                print(f"Error loading page: {e}. Retrying...")
                time.sleep(5)
                page.reload()
                page.wait_for_selector("#idTAUnitNo", timeout=90000)

        def get_text(locator):
            try:
                element = page.locator(locator)
                if element.is_visible():
                    return element.text_content().strip()
                return "Not Found"
            except Exception:
                return "Not Found"

        def get_on_hire_date():
            try:
                on_hire_date = "Not Found"
                if page.locator("#__label55").count() > 0:
                    on_hire_date = page.locator("#__label55").text_content().strip()
                elif page.locator("#idFlexBoxActivitiesBlock").count() > 0:
                    on_hire_date = page.locator("#idFlexBoxActivitiesBlock").text_content().strip()
                return on_hire_date
            except Exception as e:
                return "Not Found"

        load_page()
        text_area = page.locator("#idTAUnitNo")
        submit_button = page.locator("#idBtnUnitEnqSubmit")

        for value in entries:
            value_str = str(value)
            try:
                # Clear and reload page after each container
                text_area.fill(value_str)
                time.sleep(1)
                submit_button.click()
                page.wait_for_timeout(5000)

                if page.locator("#__mbox0-cont").is_visible():
                    print(f"No data for {value_str}")
                    data_entry = pd.DataFrame([{
                        "Input": value_str, "Unit Number": "Not Found", "Unit Type": "Not Found",
                        "Lessee": "Not Found", "Status": "Not Found", "City": "Not Found",
                        "Depot": "Not Found", "Manufacturer": "Not Found", "Manuf. Year/Month": "Not Found",
                        "On Hire Date": "Not Found"
                    }])
                    data_entry.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                    collected += 1
                    print(f"Collected: {collected} ({value_str})")

                    # ➡️ Refresh page after each entry
                    page.reload()
                    page.wait_for_selector("#idTAUnitNo", timeout=90000)
                    text_area = page.locator("#idTAUnitNo")
                    submit_button = page.locator("#idBtnUnitEnqSubmit")
                    continue

                page.wait_for_selector("#__view1-__clone1", timeout=60000)

                unit_number = get_text("#__view1-__clone1")
                unit_type = get_text("#__view1-__clone3")
                lessee = get_text("#__view1-__clone5")
                status = get_text("#__view1-__clone7")
                city = get_text("#__view1-__clone9")
                depot = get_text("#__view1-__clone11")  # Collecting Depot
                manufacturer = get_text("#idUnitStatusPanel-rows-row0-col1")  # Collecting Manufacturer
                manuf_year_month = get_text("#__view3-__clone17")

                on_hire_date = get_on_hire_date()  # Collecting On Hire Date

                # Gather all collected data into a DataFrame
                data_entry = pd.DataFrame([{
                    "Input": value_str,
                    "Unit Number": unit_number,
                    "Unit Type": unit_type,
                    "Lessee": lessee,
                    "Status": status,
                    "City": city,
                    "Depot": depot,
                    "Manufacturer": manufacturer,
                    "Manuf. Year/Month": manuf_year_month,
                    "On Hire Date": on_hire_date
                }])

                # Write data to CSV
                data_entry.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)
                collected += 1
                print(f"Collected: {collected} ({value_str})")

                # ➡️ Refresh page after each entry
                page.reload()
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                text_area = page.locator("#idTAUnitNo")
                submit_button = page.locator("#idBtnUnitEnqSubmit")

            except Exception as e:
                print(f"Error with {value_str}: {e}")
                page.reload()
                page.wait_for_selector("#idTAUnitNo", timeout=90000)
                text_area = page.locator("#idTAUnitNo")
                submit_button = page.locator("#idBtnUnitEnqSubmit")
                continue

        browser.close()
        print("Completed.")

if __name__ == "__main__":
    df = pd.read_csv("sea_combined.csv")
    output_file = "extracted_unit_numbers.csv"

    # Process entries
    new_entries = df["sea_combined"].tolist()
    process_entries(new_entries, output_file)
