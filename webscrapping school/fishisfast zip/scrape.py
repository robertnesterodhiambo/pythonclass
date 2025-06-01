import pandas as pd
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Weights to test
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
common_box_sizes = [
    (6, 6, 6),
    (8, 6, 4),
    (10, 8, 6),
    (12, 12, 8),
    (14, 10, 6),
    (16, 12, 8),
    (18, 14, 10),
    (20, 16, 12),
    (22, 18, 12),
    (24, 18, 18),
    (26, 20, 20),
    (28, 20, 20),
    (30, 20, 20),
    (36, 24, 24)
]

# Load countries
df = pd.read_csv("100 Country list 20180621.csv")
entries = df[['countryname', 'city', 'zipcode']].dropna().head(5)

# Chrome setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")
time.sleep(5)

# Setup a CSV writer to store the collected data
with open('shipping_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Country', 'City', 'Zipcode', 'Weight', 'Box Width', 'Box Depth', 'Box Height', 'Text'])  # Add box dimensions to the header

    def type_by_keystrokes(element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(0.1)

    # Process each entry (Country, City, Zipcode)
    for index, row in entries.iterrows():
        try:
            country, city, zipcode = row['countryname'], row['city'], str(row['zipcode'])

            # Country input
            country_input = driver.find_element(By.ID, "react-select-country-input")
            country_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            type_by_keystrokes(country_input, country)
            time.sleep(1)
            country_input.send_keys(Keys.ENTER)
            time.sleep(1)
            country_input.send_keys(Keys.TAB)
            time.sleep(1)

            # Determine next field type
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

            weight_input = driver.find_element(By.NAME, "weight")
            weight_input.click()
            time.sleep(1)

            # Iterate weights
            for weight in ll_lbs:
                weight_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                type_by_keystrokes(weight_input, str(weight))
                time.sleep(1)

                # Iterate through common box sizes
                for box_size in common_box_sizes:
                    width, depth, height = box_size

                    # Enter dimensions for each box size
                    driver.find_element(By.NAME, "width").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                    driver.find_element(By.NAME, "width").send_keys(str(width))
                    time.sleep(0.5)

                    driver.find_element(By.NAME, "depth").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                    driver.find_element(By.NAME, "depth").send_keys(str(depth))
                    time.sleep(0.5)

                    driver.find_element(By.NAME, "height").send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
                    driver.find_element(By.NAME, "height").send_keys(str(height))
                    time.sleep(0.5)

                    # Click the "collect" button
                    collect_button = driver.find_element(By.CSS_SELECTOR, 'div.d-grid input.btn.btn-success.btn-block[type="submit"]')
                    collect_button.click()
                    print(f"Submitted weight: {weight} and box size: {box_size}")
                    time.sleep(4)

                    # Collect data from the container
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
                                        print(f"Clicked: {elem.text}")
                                        time.sleep(0.5)

                                card_mt_0_divs = container.find_elements(By.CLASS_NAME, 'card.mt-0')
                                card_false_divs = container.find_elements(By.CLASS_NAME, 'card.false')

                                all_texts = [card.text for card in card_mt_0_divs] + [card.text for card in card_false_divs]

                                for text in all_texts:
                                    writer.writerow([country, city, zipcode, weight, width, depth, height, text])  # Include box size in the row
                                    print(f"Collected text: {text}")

                            except Exception as div_err:
                                print(f"Error collecting div data: {div_err}")

                    except Exception as e:
                        print(f"Price container error: {e}")

                    # Move to next box size
                    time.sleep(1)

                # After completing all box sizes, move to the next weight
                weight_input.send_keys(Keys.TAB)
                time.sleep(0.5)

            # After completing all weights, move to the next country, city, and zipcode
        except Exception as e:
            print(f"Error at index {index}: {e}")

input("Press Enter to exit...")
driver.quit()
