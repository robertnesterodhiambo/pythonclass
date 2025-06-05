import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Read the first 5 countries from the CSV
df = pd.read_csv('100 Country list 20180621.csv')
rows = df[['countryname', 'city', 'zipcode']].head(5)

# List of weights in pounds
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# Set up Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def initialize_page():
    driver.get("https://www.stackry.com/shipping-calculator")
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame(iframe)

    lb_label = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='boxes.[0].weightUnit-lb']")))
    driver.execute_script("arguments[0].click();", lb_label)  # Click the "lb" weight unit
    time.sleep(1)

    time.sleep(1)  # Skip the "in" (dimension unit) click

try:
    initialize_page()

    for _, row in rows.iterrows():
        retry_country = True
        weight_idx = 0  # Track the current weight index
        while retry_country:
            retry_country = False
            country = row['countryname']
            city = str(row['city']) if not pd.isna(row['city']) else ""
            zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

            print(f"\nProcessing {country} — City: {city}, Zipcode: {zipcode}")

            # Input the country, city, and zip code
            country_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "react-select-4-input")))
            country_input.clear()
            country_input.send_keys(country)
            time.sleep(1)
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

            # Loop through weights starting from the last processed weight (if any)
            for w in ll_lbs[weight_idx:]:
                try:
                    weight_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "weight")))
                    weight_input.click()
                    weight_input.send_keys(Keys.CONTROL + "a")
                    weight_input.send_keys(Keys.DELETE)
                    weight_input.send_keys(str(w))
                    print(f"Entered weight: {w} lbs")
                    time.sleep(1)
                    weight_input.send_keys(Keys.RETURN)  # Press Enter after entering the weight
                    time.sleep(3)  # Wait for the page to update
                except Exception as e:
                    print(f"Failed to enter weight {w} for {country}: {e}")

                # Skip box size entry and move to the next step if needed

                error_elements = driver.find_elements(By.CSS_SELECTOR, "p.text-red-450.mt-2")
                if any("Try again later" in e.text for e in error_elements):
                    print("⚠️ 'Try again later' message appeared. Refreshing and retrying...")
                    driver.refresh()
                    time.sleep(5)
                    initialize_page()
                    weight_idx = ll_lbs.index(w)  # Restart from current weight
                    retry_country = True
                    break

                results = driver.find_elements(By.CSS_SELECTOR, "#rateEstimateContent > div[style*='justify-content: space-between']")
                for res in results:
                    try:
                        name = res.find_element(By.TAG_NAME, "p").text.strip()
                        spans = res.find_elements(By.TAG_NAME, "span")
                        days = spans[0].text.strip() if spans else ""
                        price = res.find_element(By.TAG_NAME, "strong").text.strip()
                        print(f"💸 {name} | {days} | {price}")
                    except:
                        print("⚠️ Skipped a result block due to structure mismatch.")
                
                # After processing one weight, stop the loop and proceed to the next weight
                if retry_country:
                    break

            if not retry_country:
                print(f"✅ Finished all combinations for {country}")
                print("=" * 50)
                time.sleep(2)

finally:
    time.sleep(5)
    driver.quit()
