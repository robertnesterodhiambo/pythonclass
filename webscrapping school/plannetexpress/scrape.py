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
country_data = df[["countryname", "city", "zipcode"]].dropna().iloc[:5]
print("Loaded country, city, and zipcode data:")
print(country_data)

# Step 2: Define weight values
all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# Step 3: Chrome setup
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)
driver.get("https://planetexpress.com/postage-calculator/")

from_entries = ["Torrance, CA", "Tualatin, OR", "Fort Pierce, FL", "United Kingdom"]

try:
    for from_entry in from_entries:
        print(f"\n--- Processing 'Shipping From': {from_entry} ---")

        # Select "Shipping From"
        from_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[0]
        from_dropdown.click()
        input_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))
        input_box = input_boxes[0]
        input_box.clear()
        for ch in from_entry:
            input_box.send_keys(ch)
            time.sleep(0.1)

        time.sleep(0.7)
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
        for item in results:
            if item.text.strip().lower() == from_entry.lower():
                item.click()
                print(f"Selected 'From': {item.text}")
                break

        time.sleep(1)

        # Select "Shipping To"
        to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
        to_dropdown.click()

        for _, row in country_data.iterrows():
            country = row["countryname"]
            city = str(row["city"])
            zipcode = str(row["zipcode"])

            print(f"Shipping To: {country} | City: {city} | Zip: {zipcode}")

            input_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))
            input_box = input_boxes[1]
            input_box.clear()
            for ch in country:
                input_box.send_keys(ch)
                time.sleep(0.1)

            time.sleep(0.7)
            try:
                results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
                for item in results:
                    if item.text.strip().lower() == country.lower():
                        item.click()
                        print(f"Selected 'To': {item.text}")
                        break
            except:
                print(f"Dropdown not found for country: {country}")
                continue

            # Input city
            try:
                city_input = wait.until(EC.presence_of_element_located((By.ID, "city")))
                city_input.clear()
                for ch in city:
                    city_input.send_keys(ch)
                    time.sleep(0.05)
                print(f"Entered city: {city}")
            except:
                print("City input not found.")
                continue

            # Input postal code
            try:
                zip_input = wait.until(EC.presence_of_element_located((By.ID, "postalcode")))
                zip_input.clear()
                for ch in zipcode:
                    zip_input.send_keys(ch)
                    time.sleep(0.05)
                print(f"Entered postal code: {zipcode}")
            except:
                print("Postal code input not found.")
                continue

            # Loop through all weights
            for weight in all_lbs:
                try:
                    weight_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][weight]")))
                    weight_input.clear()
                    for ch in str(weight):
                        weight_input.send_keys(ch)
                        time.sleep(0.05)
                    print(f"Entered weight: {weight} lbs")

                    # Optional: pause briefly between weights (or submit, scrape, etc.)
                    time.sleep(0.3)

                except:
                    print("Weight input not found.")
                    continue

            time.sleep(1)
            to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
            to_dropdown.click()

except Exception as e:
    print("Error in processing:", e)

input("\nPress Enter to close browser...")
driver.quit()
