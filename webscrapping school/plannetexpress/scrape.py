import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Load CSV
df = pd.read_csv('100 Country list 20180621.csv')

# Use only the first 5 countries from the DataFrame
country_list = df["countryname"].dropna().iloc[:5].tolist()
print("Countries loaded from CSV (first 5):", country_list)

# Step 2: Chrome setup
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Step 3: Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)

# Step 4: Open the page
driver.get("https://planetexpress.com/postage-calculator/")

# === PART 1: Handle "Shipping From" (first dropdown) ===
from_entries = ["Torrance, CA", "Tualatin, OR", "Fort Pierce, FL", "United Kingdom"]

try:
    for from_entry in from_entries:
        print(f"--- Processing 'Shipping From': {from_entry} ---")

        from_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[0]
        from_dropdown.click()

        input_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))
        input_box = input_boxes[0]

        input_box.clear()
        for ch in from_entry:
            input_box.send_keys(ch)
            time.sleep(0.1)  # simulate natural typing

        time.sleep(0.7)

        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
        for item in results:
            if item.text.strip().lower() == from_entry.lower():
                print(f"Selected 'From': {item.text}")
                item.click()
                break

        time.sleep(1)

        # === PART 2: Handle "Shipping To" (second dropdown) ===
        to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
        to_dropdown.click()

        for country in country_list:
            print(f"Selecting 'Shipping To' country: {country}")

            input_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))
            input_box = input_boxes[1]

            input_box.clear()
            for ch in country:
                input_box.send_keys(ch)
                time.sleep(0.1)  # simulate typing

            time.sleep(0.7)

            try:
                results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
                found = False
                for item in results:
                    if item.text.strip().lower() == country.lower():
                        print(f"Selected 'To': {item.text}")
                        item.click()
                        found = True
                        break

                if not found:
                    print(f"Country not found in dropdown: {country}")

            except:
                print(f"No dropdown result for: {country}")

            time.sleep(1)

            # Reopen dropdown for next country
            to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
            to_dropdown.click()

        time.sleep(1)

except Exception as e:
    print("Error in dropdown processing:", e)

input("Press Enter to close browser...")
driver.quit()
