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

# List of common box sizes (length, width, height)
common_box_sizes = [
    (6, 6, 6), (8, 6, 4), (10, 8, 6), (12, 12, 8), (14, 10, 6),
    (16, 12, 8), (18, 14, 10), (20, 16, 12), (22, 18, 12),
    (24, 18, 18), (26, 20, 20), (28, 20, 20), (30, 20, 20), (36, 24, 24)
]

# Set up Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Open Stackry's shipping calculator
    driver.get("https://www.stackry.com/shipping-calculator")

    # Wait and switch to iframe
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myIframe"))
    )
    driver.switch_to.frame(iframe)

    # Select "lb" unit by clicking the visible label using JavaScript
    try:
        lb_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='boxes.[0].weightUnit-lb']"))
        )
        driver.execute_script("arguments[0].click();", lb_label)
        print("Clicked 'lb' label via JavaScript.")
        time.sleep(1)
    except Exception as e:
        print(f"Failed to click lb label via JavaScript: {e}")

    # Click "in" label for size unit (inches)
    try:
        in_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='boxes.[0].sizeUnit-in']"))
        )
        driver.execute_script("arguments[0].click();", in_label)
        print("Clicked 'in' label for size unit (inches).")
        time.sleep(1)
    except Exception as e:
        print(f"Failed to click 'in' label: {e}")

    # Loop through each country row
    for _, row in rows.iterrows():
        country = row['countryname']
        city = str(row['city']) if not pd.isna(row['city']) else ""
        zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

        print(f"\nProcessing {country} — City: {city}, Zipcode: {zipcode}")

        # Select the country
        country_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-select-4-input"))
        )
        country_input.clear()
        country_input.send_keys(country)
        time.sleep(1)
        country_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Fill city input if present
        try:
            city_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "shipToCity"))
            )
            city_input.clear()
            city_input.send_keys(city)
            print(f"Entered city: {city}")
        except:
            print("City input not present.")

        # Fill zipcode input if present
        try:
            zip_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "shipToZip"))
            )
            zip_input.clear()
            zip_input.send_keys(zipcode)
            print(f"Entered zipcode: {zipcode}")
        except:
            print("Zipcode input not present.")

        # Loop through weights
        for w in ll_lbs:
            try:
                weight_input = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "weight"))
                )
                weight_input.clear()
                weight_input.send_keys(str(w))
                print(f"Entered weight: {w} lbs")
                time.sleep(1)
            except Exception as e:
                print(f"Failed to enter weight {w} for {country}: {e}")

            for length, width, height in common_box_sizes:
                try:
                    # Get and clear dimension fields one by one
                    length_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "length")))
                    length_input.click()
                    length_input.send_keys(Keys.CONTROL + "a")
                    length_input.send_keys(Keys.DELETE)
                    length_input.send_keys(str(length))

                    width_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "width")))
                    width_input.click()
                    width_input.send_keys(Keys.CONTROL + "a")
                    width_input.send_keys(Keys.DELETE)
                    width_input.send_keys(str(width))

                    height_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "height")))
                    height_input.click()
                    height_input.send_keys(Keys.CONTROL + "a")
                    height_input.send_keys(Keys.DELETE)
                    height_input.send_keys(str(height))

                    print(f"📦 Box: {length}x{width}x{height}")

                    height_input.send_keys(Keys.RETURN)
                    time.sleep(3)

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
                except Exception as e:
                    print(f"❌ Box input or rate extraction failed: {e}")

            print(f"✅ Finished weight and box sizes for {country}")

        print(f"✅ Finished all combinations for {country}")
        print("=" * 50)
        time.sleep(2)

finally:
    time.sleep(5)
    driver.quit()
