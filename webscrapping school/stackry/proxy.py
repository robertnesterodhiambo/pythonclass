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
from selenium.webdriver.chrome.options import Options

# -------------------- OPTIONS --------------------
options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

# -------------------- CONFIG --------------------
input_csv = '100 Country list 20180621.csv'
csv_path = '/home/dragon/DATA/fishisfast.csv'
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# -------------------- LOAD DATA --------------------
df = pd.read_csv(input_csv)
rows = df[['countryname', 'city', 'zipcode']]

existing_keys = set()
if os.path.exists(csv_path):
    existing_df = pd.read_csv(csv_path)
    for _, r in existing_df.iterrows():
        key = (r['country'], r['city'], r['zipcode'], int(r['weight']))
        existing_keys.add(key)
    print(f"✅ Loaded {len(existing_keys)} previous entries.")
else:
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['country', 'city', 'zipcode', 'weight', 'service_name', 'delivery_days', 'price'])
    print("📄 Created new CSV.")

pending_tasks = []
for _, row in rows.iterrows():
    country = row['countryname']
    city = str(row['city']) if not pd.isna(row['city']) else ""
    zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""
    for weight in ll_lbs:
        key = (country, city, zipcode, weight)
        if key not in existing_keys:
            pending_tasks.append((row, weight))

print(f"🚀 {len(pending_tasks)} new combinations to scrape.")

# -------------------- SETUP --------------------
def initialize_page():
    driver.get("https://www.stackry.com/shipping-calculator")
    wait.until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame("myIframe")
    lb_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='boxes.[0].weightUnit-lb']")))
    driver.execute_script("arguments[0].click();", lb_label)
    time.sleep(1)

def save_result(row, weight, service_name, delivery_days, price):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([row['countryname'], row['city'], row['zipcode'], weight, service_name, delivery_days, price])

# -------------------- MANUAL SCRAPING --------------------
try:
    initialize_page()

    for idx, (row, weight) in enumerate(pending_tasks):
        country = row['countryname']
        city = str(row['city']) if not pd.isna(row['city']) else ""
        zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

        print(f"\n➡️ Prepare input in browser for:")
        print(f"   Country: {country}")
        print(f"   City: {city}")
        print(f"   Zipcode: {zipcode}")
        print(f"   Weight: {weight} lbs")
        input("🔵 Press ENTER once you have entered this manually and the rates are visible...")

        try:
            driver.switch_to.default_content()
            time.sleep(2)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[style*='justify-content: space-between; padding: 0.75rem;']"))
            )
            result_blocks = driver.find_elements(By.CSS_SELECTOR, "div[style*='justify-content: space-between; padding: 0.75rem;']")
            found = False

            for i in range(len(result_blocks)):
                try:
                    # Re-fetch every time to avoid stale reference
                    result_blocks = driver.find_elements(By.CSS_SELECTOR, "div[style*='justify-content: space-between; padding: 0.75rem;']")
                    res = result_blocks[i]

                    service_name = res.find_element(By.XPATH, ".//p[contains(@style,'font-size')]").text.strip()
                    delivery_days = res.find_element(By.XPATH, ".//span[contains(@style,'text-align: end')]").text.strip()
                    price = res.find_element(By.XPATH, ".//strong[contains(@style,'font-weight')]").text.strip()
                    print(f"💸 {service_name} | {delivery_days} | {price}")
                    save_result(row, weight, service_name, delivery_days, price)
                    found = True
                except Exception as e:
                    print(f"⚠️ Error parsing result {i}: {e}")

            if not found:
                print("⚠️ No shipping results found.")

            driver.switch_to.frame("myIframe")

        except Exception as e:
            print(f"❌ Error scraping results: {e}")
            driver.refresh()
            time.sleep(5)
            initialize_page()

finally:
    driver.quit()
    print("✅ Done and browser closed.")
