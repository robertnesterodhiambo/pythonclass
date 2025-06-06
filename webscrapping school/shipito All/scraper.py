from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Setup Chrome
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Uncomment to run headless
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# Load input
df = pd.read_csv("100 Country list 20180621.csv")
output_file = "shipto.xlsx"
fail_file = "fail.xlsx"
all_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
final_output = []
fail = []

# Resume logic
if os.path.exists(output_file):
    existing = pd.read_excel(output_file)
    processed = set(zip(existing["Receiving Country"], existing["Receiving City"], existing["Receiving Zipcode"]))
else:
    processed = set()

# Open Shipito
driver.get("https://www.shipito.com/en/shipping-calculator")

# Main loop
for index, row in df.iterrows():
    key = (str(row["countryname"]).strip(), str(row["city"]).strip(), str(row["zipcode"]).strip())
    if key in processed:
        print(f"✅ Already processed: {key}")
        continue

    for attempt in range(1, 4):
        print(f"\nProcessing {index}: {key} | Attempt {attempt}")
        try:
            driver.get("https://www.shipito.com/en/shipping-calculator")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class='btn dropdown-toggle']")))

            # Select warehouse
            driver.execute_script("window.scrollTo(0, 400)")
            driver.find_element(By.XPATH, "//button[@class='btn dropdown-toggle']").click()
            driver.find_element(By.XPATH, "//a[@data-value='7']").click()
            time.sleep(2)

            # Type country (no selection logic)
            driver.execute_script("window.scrollTo(0, 950)")
            driver.find_element(By.XPATH, "//li[@class='dropdown st-selected-country']").click()
            time.sleep(1)
            country_input = driver.find_elements(By.XPATH, "//input[@class='form-control st-country-filter']")[1]
            country_input.clear()
            time.sleep(0.5)
            country_input.send_keys(str(row["countryname"]).strip())
            time.sleep(1)  # Give time for dropdown to auto-select silently

            # Fill city and zip
            driver.find_element(By.NAME, "shippingcalculator.city").clear()
            driver.find_element(By.NAME, "shippingcalculator.city").send_keys(str(row["city"]).strip())
            driver.find_element(By.NAME, "shippingcalculator.postalcode").clear()
            driver.find_element(By.NAME, "shippingcalculator.postalcode").send_keys(str(row["zipcode"]).strip())

            # Weights
            for weight in all_lbs:
                weight_input = driver.find_element(By.NAME, "shippingcalculator.scaleweight_val")
                weight_input.clear()
                weight_input.send_keys(str(weight))

                driver.find_element(By.XPATH, "//button[@class='btn btn-secondary btn-calculator']").click()
                wait = WebDriverWait(driver, 15)
                wait.until(EC.presence_of_element_located((By.XPATH, "//table[@class='table quotes-table']")))

                table = driver.find_element(By.XPATH, "//table[@class='table quotes-table']")
                if len(table.text.strip()) == 0:
                    final_output.append(["California USA", *key, weight])
                    print("⚠️ No result for:", key, weight)
                else:
                    for row_body in table.find_elements(By.XPATH, "tbody"):
                        for tr in row_body.find_elements(By.XPATH, "tr"):
                            if tr.text.strip():
                                tds = tr.find_elements(By.TAG_NAME, "td")
                                data = [td.text.strip() for td in tds]
                                if len(data) >= 6:
                                    final_output.append(["California USA", *key, weight, data[0], *data[1].split(" ", 1), *data[2:]])
                                    print(["California USA", *key, weight, data[0], *data[1].split(" ", 1), *data[2:]])

            # Save
            df_out = pd.DataFrame(final_output, columns=[
                "Sending Warehouse", "Receiving Country", "Receiving City", "Receiving Zipcode", "Weight in (LBS)",
                "Shipping Method", "Postage", "Postage Currency", "Estimated Delivery Time", "Insurance",
                "Tracking", "Weight", "Limits"
            ])
            df_out.to_excel(output_file, index=False)
            break

        except Exception as e:
            print(f"❌ Error: {e}")
            if attempt == 3:
                print(f"⛔ Skipping: {key}")
                fail.append(index)
            time.sleep(2)

# Save failures
if fail:
    pd.DataFrame(fail, columns=["Failed Indexes"]).to_excel(fail_file, index=False)

driver.quit()
