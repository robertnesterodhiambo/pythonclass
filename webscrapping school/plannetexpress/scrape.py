import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# === Step 1: Load CSV ===
df = pd.read_csv('100 Country list 20180621.csv')
country_data = df[["countryname", "city", "zipcode"]].dropna().iloc[:5]

# === Step 2: Define weights, dimensions, values ===
all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
package_sizes = [
    (12, 8, 1)
]
goods_values = [v for v in range(10, 20, 10)]  # 10, 20, 30, ..., 100


# === Step 3: Set up Chrome ===
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)
driver.get("https://planetexpress.com/postage-calculator/")

from_entries = ["Torrance, CA", "Tualatin, OR", "Fort Pierce, FL", "United Kingdom"]

# === Step 4: Main Automation ===
try:
    for from_entry in from_entries:
        print(f"\n--- Shipping From: {from_entry} ---")

        # Select Shipping From
        from_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[0]
        from_dropdown.click()
        from_input = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))[0]
        from_input.clear()
        for ch in from_entry:
            from_input.send_keys(ch)
            time.sleep(0.1)

        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
        for item in results:
            if item.text.strip().lower() == from_entry.lower():
                item.click()
                break

        time.sleep(1)

        to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
        to_dropdown.click()

        for _, row in country_data.iterrows():
            country = row["countryname"]
            city = str(row["city"])
            zipcode = str(row["zipcode"])

            # Select Shipping To
            to_input = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chosen-search-input")))[1]
            to_input.clear()
            for ch in country:
                to_input.send_keys(ch)
                time.sleep(0.1)

            time.sleep(0.7)
            try:
                results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))
                for item in results:
                    if item.text.strip().lower() == country.lower():
                        item.click()
                        break
            except:
                continue

            try:
                city_input = wait.until(EC.presence_of_element_located((By.ID, "city")))
                city_input.clear()
                for ch in city:
                    city_input.send_keys(ch)
                    time.sleep(0.05)
            except:
                continue

            try:
                zip_input = wait.until(EC.presence_of_element_located((By.ID, "postalcode")))
                zip_input.clear()
                for ch in zipcode:
                    zip_input.send_keys(ch)
                    time.sleep(0.05)
            except:
                continue

            for weight in all_lbs:
                try:
                    weight_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][weight]")))
                    weight_input.clear()
                    for ch in str(weight):
                        weight_input.send_keys(ch)
                        time.sleep(0.05)
                except:
                    continue

                for size in package_sizes:
                    length, width, height = size
                    try:
                        length_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][length]")))
                        length_input.clear()
                        length_input.send_keys(str(length))

                        width_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][width]")))
                        width_input.clear()
                        width_input.send_keys(str(width))

                        height_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][height]")))
                        height_input.clear()
                        height_input.send_keys(str(height))
                    except:
                        continue

                    for value in goods_values:
                        try:
                            value_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][value]")))
                            value_input.clear()
                            for ch in str(value):
                                value_input.send_keys(ch)
                                time.sleep(0.05)

                            value_input.send_keys(Keys.TAB)  # Ensure value input loses focus
                            time.sleep(0.3)

                            # Click the "Calculate" button reliably using JavaScript
                            calculate_button = driver.find_element(By.NAME, "calculate")
                            driver.execute_script("arguments[0].click();", calculate_button)

                            # Wait for 5 seconds after clicking the Calculate button
                            time.sleep(5)

                            print(f"Submitted: From={from_entry}, To={country}, City={city}, ZIP={zipcode}, Wt={weight}, Size={size}, Value=${value}")
                            time.sleep(0.5)

                        except Exception as e:
                            print(f"Failed to submit value ${value}: {e}")
                            continue

            to_dropdown = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".chosen-container")))[1]
            to_dropdown.click()

except Exception as e:
    print("General Error:", e)

input("\nPress Enter to exit and close the browser...")
driver.quit()
