import pandas as pd
import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- CONFIG --------------------
input_csv = '100 Country list 20180621.csv'
csv_path = '/home/dragon/DATA/fishisfast.csv'

# Weights in pounds
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# -------------------- LOAD DATA --------------------
df = pd.read_csv(input_csv)
rows = df[['countryname', 'city', 'zipcode']].head(5)

# Load existing completed entries
existing_keys = set()
if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path)
    for _, r in existing_df.iterrows():
        key = (r['country'], r['city'], r['zipcode'], int(r['weight']))
        existing_keys.add(key)
    print(f"✅ Loaded {len(existing_keys)} previously collected entries.")
else:
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'city', 'zipcode', 'weight', 'service_name', 'delivery_days', 'price'])
    print("📄 Created new result CSV.")

# Precompute all combinations
pending_tasks = []
for _, row in rows.iterrows():
    country = row['countryname']
    city = str(row['city']) if not pd.isna(row['city']) else ""
    zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""
    for weight in ll_lbs:
        key = (country, city, zipcode, weight)
        if key not in existing_keys:
            pending_tasks.append((row, weight))

print(f"🚀 Ready to scrape {len(pending_tasks)} new combinations.")

# -------------------- SETUP SELENIUM --------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

iframe = None

def initialize_page():
    global iframe
    driver.get("https://www.stackry.com/shipping-calculator")
    iframe = wait.until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame(iframe)
    lb_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='boxes.[0].weightUnit-lb']")))
    driver.execute_script("arguments[0].click();", lb_label)
    time.sleep(1)

def save_result(row, weight, service_name, delivery_days, price):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([row['countryname'], row['city'], row['zipcode'], weight, service_name, delivery_days, price])

# -------------------- SCRAPING --------------------
try:
    initialize_page()
    last_country = last_city = last_zip = None

    for row, weight in pending_tasks:
        country = row['countryname']
        city = str(row['city']) if not pd.isna(row['city']) else ""
        zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

        if (country != last_country) or (city != last_city) or (zipcode != last_zip):
            print(f"\n🌍 Switching to {country} — City: {city}, Zip: {zipcode}")
            country_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
            country_input.clear()
            for ch in country:
                country_input.send_keys(ch)
                time.sleep(0.1)
            country_input.send_keys(Keys.RETURN)
            time.sleep(2)

            try:
                city_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "shipToCity")))
                city_input.clear()
                city_input.send_keys(city)
                print(f"📝 Entered city: {city}")
            except:
                print("⚠️ City input not present.")

            try:
                zip_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "shipToZip")))
                zip_input.clear()
                zip_input.send_keys(zipcode)
                print(f"📝 Entered zip: {zipcode}")
            except:
                print("⚠️ Zipcode input not present.")

            last_country, last_city, last_zip = country, city, zipcode

        try:
            weight_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "weight")))
            weight_input.click()
            weight_input.send_keys(Keys.CONTROL + "a")
            weight_input.send_keys(Keys.DELETE)
            weight_input.send_keys(str(weight))
            print(f"⚖️ Weight: {weight} lbs")
            weight_input.send_keys(Keys.RETURN)
            time.sleep(3)

            error_elements = driver.find_elements(By.CSS_SELECTOR, "p.text-red-450.mt-2")
            if any("Try again later" in e.text for e in error_elements):
                print("⚠️ 'Try again later' message. Refreshing...")
                driver.refresh()
                time.sleep(5)
                initialize_page()
                last_country = last_city = last_zip = None  # force re-input on retry
                continue

            driver.switch_to.default_content()
            time.sleep(2)

            result_blocks = driver.find_elements(By.CSS_SELECTOR, "div[style*='justify-content: space-between; padding: 0.75rem;']")
            for res in result_blocks:
                try:
                    service_name = res.find_element(By.XPATH, ".//p[contains(@style,'font-size')]").text.strip()
                    delivery_days = res.find_element(By.XPATH, ".//span[contains(@style,'text-align: end')]").text.strip()
                    price = res.find_element(By.XPATH, ".//strong[contains(@style,'font-weight')]").text.strip()
                    print(f"💸 {service_name} | {delivery_days} | {price}")
                    save_result(row, weight, service_name, delivery_days, price)
                except Exception as e:
                    print(f"⚠️ Error reading service block: {e}")

            driver.switch_to.frame(iframe)

        except Exception as e:
            print(f"❌ Error on weight {weight} lbs for {country}: {e}")
            driver.switch_to.frame(iframe)

finally:
    time.sleep(5)
    driver.quit()
