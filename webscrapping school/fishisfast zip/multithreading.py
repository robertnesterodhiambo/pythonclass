import pandas as pd
import time
import csv
import os
import threading
from queue import Queue
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

# Output file and existing entry check
output_file = '/home/dragon/DATA/shipping_data.csv'
file_exists = os.path.isfile(output_file)
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

# Prepare queue of combinations to process
todo_combinations = []
for _, row in entries.iterrows():
    country, city, zipcode = row['countryname'], row['city'], str(row['zipcode'])
    for weight in ll_lbs:
        for width, depth, height in common_box_sizes:
            key = (country, city, zipcode, float(weight), int(width), int(depth), int(height))
            if key not in existing_entries:
                todo_combinations.append((country, city, zipcode, weight, width, depth, height))

if not todo_combinations:
    print("🎉 All data has already been collected. Exiting.")
    exit()

# Threading setup
lock = threading.Lock()
task_queue = Queue()
for combo in todo_combinations:
    task_queue.put(combo)

# CSV header setup
if not file_exists:
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Country', 'City', 'Zipcode', 'Weight', 'Box Width', 'Box Depth', 'Box Height',
                         'Method', 'Price', 'Estimated Delivery', 'Max Weight', 'Dimensional Weight',
                         'Tracking', 'Size', 'Insurance'])

def type_by_keystrokes(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

def worker(thread_id):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=2560,1440")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.fishisfast.com/en/shipping_calculator")
    time.sleep(5)
    current_location = (None, None, None)

    while not task_queue.empty():
        try:
            combo = task_queue.get_nowait()
        except:
            break

        country, city, zipcode, weight, width, depth, height = combo
        try:
            with lock:
                print(f"🧵 Thread-{thread_id} processing {country}, {city}, {zipcode}, {weight} lbs, {width}x{depth}x{height}")

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

            driver.find_element(By.NAME, "weight").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "weight").send_keys(str(weight))
            time.sleep(0.5)

            driver.find_element(By.NAME, "width").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "width").send_keys(str(width))
            time.sleep(0.5)

            driver.find_element(By.NAME, "depth").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "depth").send_keys(str(depth))
            time.sleep(0.5)

            driver.find_element(By.NAME, "height").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            driver.find_element(By.NAME, "height").send_keys(str(height))
            time.sleep(0.5)

            driver.find_element(By.CSS_SELECTOR, 'div.d-grid input.btn.btn-success.btn-block[type="submit"]').click()
            time.sleep(9)

            error_detected = False
            try:
                error_div = driver.find_element(By.CLASS_NAME, "alert-danger")
                if "there are no valid shipping methods" in error_div.text.lower():
                    with lock:
                        with open(output_file, mode='a', newline='') as f:
                            csv.writer(f).writerow([country, city, zipcode, weight, width, depth, height] + ["No Data"] * 8)
                    error_detected = True
            except:
                pass

            if not error_detected:
                try:
                    containers = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.col-12.col-sm-6.col-md-7.col-lg-8')))
                    for container in containers:
                        dollar_elements = container.find_elements(By.TAG_NAME, "b")
                        for elem in dollar_elements:
                            if "$" in elem.text:
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elem)
                                time.sleep(0.3)
                                elem.click()
                                time.sleep(0.5)

                        card_mt_0 = container.find_elements(By.CLASS_NAME, 'card.mt-0')
                        card_false = container.find_elements(By.CLASS_NAME, 'card.false')
                        all_texts = [card.text for card in card_mt_0 + card_false]

                        with lock:
                            with open(output_file, mode='a', newline='') as f:
                                writer = csv.writer(f)
                                for text in all_texts:
                                    writer.writerow([country, city, zipcode, weight, width, depth, height, text])
                except Exception as e:
                    print(f"❌ Thread-{thread_id} price container error: {e}")

        except Exception as e:
            print(f"❌ Thread-{thread_id} combo error: {e}")

    driver.quit()

# Launch threads
threads = []
max_threads = 10
for i in range(min(max_threads, task_queue.qsize())):
    t = threading.Thread(target=worker, args=(i+1,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("✅ All threads completed.")
