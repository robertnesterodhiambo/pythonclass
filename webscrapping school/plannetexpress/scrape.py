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
import csv
import os

# === Step 1: Load CSV ===
df = pd.read_csv('100 Country list 20180621.csv')
country_data = df[["countryname", "city", "zipcode"]].dropna()

# === Step 2: Define weights, dimensions, values ===
all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
package_sizes = [
    (12, 8, 1)
]
goods_values = [v for v in range(10, 20, 10)]  # 10, 20

# === Step 3: Set up Chrome ===
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new") 
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 15)
driver.get("https://planetexpress.com/postage-calculator/")

from_entries = ["United Kingdom"] #,"Fort Pierce, FL", "United Kingdom","Torrance, CA", "Tualatin, OR"]

# === Step 3.5: Prepare CSV File ===
output_file = 'shipping_results.csv'
write_header = not os.path.exists(output_file)
if write_header:
    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "From", "To Country", "To City", "Postal Code",
            "Weight (lbs)", "Length", "Width", "Height", "Value (USD)",
            "Shipping Method", "Estimated Delivery", "Price", "Currency", "Insurance Text", "Insurance Amount"
        ])

# === Step 3.6: Load existing results to avoid duplicates ===
processed_keys = set()
if os.path.exists(output_file):
    with open(output_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            key = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])  # from, to_country, city, zip, weight, length, width, height, value
            processed_keys.add(tuple(key))

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
                        entry_key = (from_entry, country, city, zipcode, str(weight), str(length), str(width), str(height), str(value))
                        if entry_key in processed_keys:
                            print(f"Skipping already processed entry: {entry_key}")
                            continue

                        try:
                            value_input = wait.until(EC.presence_of_element_located((By.NAME, "packages[0][value]")))
                            value_input.clear()
                            for ch in str(value):
                                value_input.send_keys(ch)
                                time.sleep(0.05)

                            value_input.send_keys(Keys.TAB)
                            time.sleep(0.3)

                            calculate_button = driver.find_element(By.NAME, "calculate")
                            driver.execute_script("arguments[0].click();", calculate_button)

                            time.sleep(5)

                            # === Step 5: Extract shipping information ===
                            try:
                                shipping_rates_div = wait.until(EC.presence_of_element_located((By.ID, "shippingRates")))
                                carriers = shipping_rates_div.find_elements(By.CLASS_NAME, "carrier")

                                for carrier in carriers:
                                    shipping_method = carrier.find_element(By.CSS_SELECTOR, ".dataContainer").text.strip().split("\n")[0]
                                    estimated_delivery_time = carrier.find_element(By.CSS_SELECTOR, ".dataContainer em").text.strip()
                                    price = carrier.find_element(By.CSS_SELECTOR, ".priceContainer strong").text.strip()
                                    currency = price.split(" ")[-1]
                                    insurance_text = carrier.find_element(By.CSS_SELECTOR, ".priceContainer small").text.strip()

                                    insurance_amount = 0.0
                                    if 'Insurance' in insurance_text:
                                        try:
                                            insurance_amount_str = insurance_text.split(" ")[-2]
                                            insurance_amount = float(insurance_amount_str)
                                        except ValueError:
                                            insurance_amount = 0.0

                                    print(f"Shipping Method: {shipping_method}")
                                    print(f"Estimated Delivery Time: {estimated_delivery_time}")
                                    print(f"Price: {price}")
                                    print(f"Currency: {currency}")
                                    print(f"Insurance: {insurance_text}")
                                    print(f"Insurance Amount: {insurance_amount}\n")

                                    # === Save data to CSV ===
                                    with open(output_file, mode='a', newline='', encoding='utf-8') as csvfile:
                                        writer = csv.writer(csvfile)
                                        writer.writerow([
                                            from_entry, country, city, zipcode,
                                            weight, length, width, height, value,
                                            shipping_method, estimated_delivery_time,
                                            price, currency, insurance_text, insurance_amount
                                        ])

                                    # Add to processed set to avoid reprocessing in same run
                                    processed_keys.add(entry_key)

                            except Exception as e:
                                print(f"Error extracting shipping rates: {e}")

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
