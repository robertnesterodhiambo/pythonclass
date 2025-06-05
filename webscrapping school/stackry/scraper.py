import pandas as pd
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Read countries
df = pd.read_csv('100 Country list 20180621.csv')
rows = df[['countryname', 'city', 'zipcode']].head(5)

# Weights in pounds
ll_lbs = [1, 2, 3, 4, 5, 10]

# Path to save results
csv_path = '/home/dragon/DATA/fishisfast.csv'

# Write headers to CSV if it doesn't exist
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['country', 'city', 'zipcode', 'weight', 'service_name', 'delivery_days', 'price'])

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# Declare iframe globally
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

try:
    initialize_page()

    for _, row in rows.iterrows():
        retry_country = True
        while retry_country:
            retry_country = False
            country = row['countryname']
            city = str(row['city']) if not pd.isna(row['city']) else ""
            zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

            print(f"\nProcessing {country} — City: {city}, Zipcode: {zipcode}")

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
                print(f"Entered city: {city}")
            except:
                print("City input not present.")

            try:
                zip_input = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "shipToZip")))
                zip_input.clear()
                zip_input.send_keys(zipcode)
                print(f"Entered zipcode: {zipcode}")
            except:
                print("Zipcode input not present.")

            for weight in ll_lbs:
                try:
                    weight_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "weight")))
                    weight_input.click()
                    weight_input.send_keys(Keys.CONTROL + "a")
                    weight_input.send_keys(Keys.DELETE)
                    weight_input.send_keys(str(weight))
                    print(f"Entered weight: {weight} lbs")
                    weight_input.send_keys(Keys.RETURN)
                    time.sleep(3)

                    # Check for 'Try again later'
                    error_elements = driver.find_elements(By.CSS_SELECTOR, "p.text-red-450.mt-2")
                    if any("Try again later" in e.text for e in error_elements):
                        print("⚠️ 'Try again later' message appeared. Refreshing and retrying...")
                        driver.refresh()
                        time.sleep(5)
                        initialize_page()
                        retry_country = True
                        break

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
                            print(f"⚠️ Failed to parse result block: {e}")

                    driver.switch_to.frame(iframe)

                except Exception as e:
                    print(f"❌ Weight {weight} failed for {country}: {e}")
                    driver.switch_to.frame(iframe)

finally:
    time.sleep(5)
    driver.quit()
