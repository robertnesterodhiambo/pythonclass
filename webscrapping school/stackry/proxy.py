import pandas as pd
import csv
import time
import os
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# -------------------- LOAD PROXIES --------------------
def fetch_proxies():
    urls = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
    ]
    proxies = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=10)
            proxies += resp.text.strip().split('\n')
        except:
            continue
    print(f"🧩 Loaded {len(proxies)} proxies.")
    return proxies

proxy_list = fetch_proxies()

# -------------------- SELENIUM WITH PROXY --------------------
def get_driver_with_proxy(proxy=None):
    chrome_options = Options()
#    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1920,1080')
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_working_driver():
    for attempt in range(10):
        proxy = random.choice(proxy_list)
        print(f"🌐 Trying proxy: {proxy}")
        try:
            driver = get_driver_with_proxy(proxy)
            driver.set_page_load_timeout(20)
            driver.get("https://www.stackry.com/shipping-calculator")
            if "Shipping Calculator" in driver.page_source:
                print("✅ Proxy works!")
                return driver
            else:
                driver.quit()
        except Exception as e:
            print(f"❌ Proxy failed: {e}")
            try:
                driver.quit()
            except:
                pass
    raise Exception("No working proxy found.")

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

# -------------------- SCRAPER --------------------
driver = get_working_driver()
wait = WebDriverWait(driver, 10)
iframe = None
last_input = None

def initialize_page():
    global iframe
    driver.get("https://www.stackry.com/shipping-calculator")
    iframe = wait.until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame(iframe)
    lb_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='boxes.[0].weightUnit-lb']")))
    driver.execute_script("arguments[0].click();", lb_label)
    time.sleep(1)

def enter_location(country, city, zipcode):
    global last_input
    if last_input == (country, city, zipcode):
        return
    print(f"\n🌍 {country} | City: {city} | Zip: {zipcode}")
    country_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
    country_input.clear()
    for ch in country:
        country_input.send_keys(ch)
        time.sleep(0.2)
    time.sleep(1)
    country_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    country_input.send_keys(Keys.RETURN)
    print(f"🏁 Selected country: {country}")
    time.sleep(2)
    try:
        city_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "shipToCity")))
        city_input.clear()
        for ch in city:
            city_input.send_keys(ch)
            time.sleep(0.1)
        print(f"🏙️ Entered city: {city}")
        time.sleep(1)
    except:
        print("⚠️ City input missing.")
    try:
        zip_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "shipToZip")))
        zip_input.clear()
        for ch in zipcode:
            zip_input.send_keys(ch)
            time.sleep(0.1)
        print(f"🏷️ Entered zip: {zipcode}")
        time.sleep(1)
    except:
        print("⚠️ Zipcode input missing.")
    last_input = (country, city, zipcode)

def save_result(row, weight, service_name, delivery_days, price):
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([row['countryname'], row['city'], row['zipcode'], weight, service_name, delivery_days, price])

# -------------------- MAIN LOOP --------------------
try:
    initialize_page()
    for idx, (row, weight) in enumerate(pending_tasks):
        country = row['countryname']
        city = str(row['city']) if not pd.isna(row['city']) else ""
        zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""
        if idx % 20 == 0 and idx > 0:
            print("⏳ Sleeping to avoid rate-limiting...")
            time.sleep(15)
        while True:
            try:
                enter_location(country, city, zipcode)
                weight_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "weight")))
                weight_input.click()
                weight_input.send_keys(Keys.CONTROL + "a")
                weight_input.send_keys(Keys.DELETE)
                weight_input.send_keys(str(weight))
                print(f"⚖️ {weight} lbs")
                weight_input.send_keys(Keys.RETURN)
                time.sleep(5)
                driver.switch_to.default_content()
                time.sleep(2)
                result_blocks = driver.find_elements(By.CSS_SELECTOR, "div[style*='justify-content: space-between; padding: 0.75rem;']")
                found = False
                for res in result_blocks:
                    try:
                        service_name = res.find_element(By.XPATH, ".//p[contains(@style,'font-size')]").text.strip()
                        delivery_days = res.find_element(By.XPATH, ".//span[contains(@style,'text-align: end')]").text.strip()
                        price = res.find_element(By.XPATH, ".//strong[contains(@style,'font-weight')]").text.strip()
                        print(f"💸 {service_name} | {delivery_days} | {price}")
                        save_result(row, weight, service_name, delivery_days, price)
                        found = True
                    except Exception as e:
                        print(f"⚠️ Error parsing result: {e}")
                driver.switch_to.frame(iframe)
                if not found:
                    print("⚠️ No shipping results found.")
                break
            except Exception as e:
                print(f"❌ Error for {country}, {city}, {zipcode}, {weight} lbs: {e}")
                driver.refresh()
                time.sleep(5)
                initialize_page()
                last_input = None
                continue
finally:
    time.sleep(5)
    driver.quit()
