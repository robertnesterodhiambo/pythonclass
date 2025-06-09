import pandas as pd
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Weights and box sizes
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
common_box_sizes = [
    (6, 6, 6), (8, 6, 4), (10, 8, 6), (12, 12, 8), (14, 10, 6),
    (16, 12, 8), (18, 14, 10), (20, 16, 12), (22, 18, 12),
    (24, 18, 18), (26, 20, 20), (28, 20, 20), (30, 20, 20), (36, 24, 24)
]

# Load destination data
df = pd.read_csv("100 Country list 20180621.csv")
entries = df[['countryname', 'city', 'zipcode']].dropna()

# Find the middle index
middle_index = 72

# Process from the middle to the end
entries = entries.iloc[middle_index:]

# Output file and existing entry check
output_file = '/home/dragon/DATA/shipping_data.csv'
file_exists = os.path.isfile(output_file)

# Load previously collected entries
existing_entries = set()
if file_exists:
    with open(output_file, mode='r', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                key = (row[0], row[1], row[2], float(row[3]), int(row[4]), int(row[5]), int(row[6]))
                existing_entries.add(key)
            except:
                continue

# Pre-check and skip already fully processed locations
todo_combinations = []
for _, row in entries.iterrows():
    country, city, zipcode = row['countryname'], row['city'], str(row['zipcode'])
    all_covered = True
    for weight in ll_lbs:
        for width, depth, height in common_box_sizes:
            key = (country, city, zipcode, float(weight), int(width), int(depth), int(height))
            if key not in existing_entries:
                todo_combinations.append((country, city, zipcode, weight, width, depth, height))
                all_covered = False
    if all_covered:
        print(f"✅ Skipping {country}, {city}, {zipcode} — already fully collected.")
    else:
        print(f"🔍 Will process {country}, {city}, {zipcode} — missing combinations.")

if not todo_combinations:
    print("🎉 All data has already been collected. Exiting.")
    exit()

# Setup options and start browser
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=2560,1440")
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")
time.sleep(5)
driver.save_screenshot("/home/dragon/page_load_confirm.png")
print("📸 Screenshot saved: page_load_confirm.png")

# CSV writer setup
with open(output_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Country', 'City', 'Zipcode', 'Weight', 'Box Width', 'Box Depth', 'Box Height',
                         'Method', 'Price', 'Estimated Delivery', 'Max Weight', 'Dimensional Weight',
                         'Tracking', 'Size', 'Insurance'])

    def type_by_keystrokes(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(0.1)

    current_location = (None, None, None)
    restart_counter = 0  # Track how many combos processed

    for combo in todo_combinations:
        country, city, zipcode, weight, width, depth, height = combo
        try:
            if (country, city, zipcode) != current_location:
                country_input = driver.find_element(By.ID, "react-select-country-input")
                country_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                type_by_keystrokes(country_input, country)
                time.sleep(1)
                country_input.send_keys(Keys.ENTER)
                time.sleep(2)
                country_input.send_keys(Keys.TAB)
                time.sleep(1)

                form = driver.find_element(By.TAG_NAME, "form")
                labels = form.find_elements(By.CLASS_NAME, "form-label")
                label_texts = [label.text.lower() for label in labels]
                field_type = "city" if any("city" in text for text in label_texts) else "zipcode"

                active_input = driver.switch_to.active_element
                value = city if field_type == "city" else zipcode
                active_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                type_by_keystrokes(active_input, value)
                if field_type == "city":
                    active_input.send_keys(Keys.ENTER)
                time.sleep(0.5)

                for _ in range(3):
                    active_input.send_keys(Keys.TAB)
                    time.sleep(0.5)

                current_location = (country, city, zipcode)
                weight_input = driver.find_element(By.NAME, "weight")
                weight_input.click()
                time.sleep(1)

            weight_input = driver.find_element(By.NAME, "weight")
            weight_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            type_by_keystrokes(weight_input, str(weight))
            time.sleep(1)

            driver.find_element(By.NAME, "width").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "width").send_keys(str(width))
            time.sleep(0.5)

            driver.find_element(By.NAME, "depth").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "depth").send_keys(str(depth))
            time.sleep(0.5)

            driver.find_element(By.NAME, "height").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "height").send_keys(str(height))
            time.sleep(0.5)

            collect_button = driver.find_element(By.CSS_SELECTOR, 'div.d-grid input.btn.btn-success.btn-block[type="submit"]')
            collect_button.click()
            time.sleep(4)
            print(f"🚀 Submitted: {country}, {city}, {zipcode}, {weight} lbs, Box: {width}x{depth}x{height}")
            time.sleep(6)

            error_detected = False
            try:
                error_div = driver.find_element(By.CLASS_NAME, "alert-danger")
                if "there are no valid shipping methods" in error_div.text.lower():
                    writer.writerow([country, city, zipcode, weight, width, depth, height] + ["No Data"] * 8)
                    print(f"⚠️ No valid shipping methods for {country}, {city}, {zipcode}, {weight} lbs, Box: {width}x{depth}x{height}")
                    error_detected = True
            except:
                pass

            if not error_detected:
                try:
                    price_containers = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.col-12.col-sm-6.col-md-7.col-lg-8'))
                    )
                    for container in price_containers:
                        try:
                            dollar_elements = container.find_elements(By.TAG_NAME, "b")
                            for elem in dollar_elements:
                                if "$" in elem.text:
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                                    time.sleep(0.3)
                                    elem.click()
                                    print(f"💲 Clicked: {elem.text}")
                                    time.sleep(0.5)

                            card_mt_0_divs = container.find_elements(By.CLASS_NAME, 'card.mt-0')
                            card_false_divs = container.find_elements(By.CLASS_NAME, 'card.false')
                            all_texts = [card.text for card in card_mt_0_divs] + [card.text for card in card_false_divs]

                            for text in all_texts:
                                writer.writerow([country, city, zipcode, weight, width, depth, height, text])
                                print(f"📦 Collected text for {weight} lbs, {width}x{depth}x{height}")

                        except Exception as div_err:
                            print(f"❌ Modal error: {div_err}")
                except Exception as e:
                    print(f"❌ Price container error: {e}")

            restart_counter += 1
            if restart_counter >= 100:
                print("🔁 Restarting browser to clear memory...")
                driver.quit()
                time.sleep(2)
                driver = webdriver.Chrome(options=options)
                driver.get("https://www.fishisfast.com/en/shipping_calculator")
                time.sleep(5)
                driver.save_screenshot("/home/dragon/page_load_confirm_after_restart.png")
                print("📸 Screenshot saved after restart")
                current_location = (None, None, None)
                restart_counter = 0

            time.sleep(1)

        except Exception as e:
            print(f"❌ Error with {combo}: {e}")

input("Press Enter to exit...")
driver.quit()
