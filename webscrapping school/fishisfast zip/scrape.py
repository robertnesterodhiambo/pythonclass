import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Weights to test
ll_lbs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 18, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]

# Load countries
df = pd.read_csv("100 Country list 20180621.csv")
entries = df[['countryname', 'city', 'zipcode']].dropna().head(5)

# Chrome setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")
time.sleep(5)

def type_by_keystrokes(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

# Process each entry
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

            submit = driver.find_element(By.CSS_SELECTOR, 'div.d-grid input.btn.btn-success.btn-block[type="submit"]')
            submit.click()
            print(f"Submitted weight: {weight}")
            time.sleep(4)

            # New: Click all $ elements inside the specified divs
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
                    except Exception as click_err:
                        print(f"Click error in container: {click_err}")
            except Exception as e:
                print(f"Price container error: {e}")

            weight_input.send_keys(Keys.TAB)
            time.sleep(0.5)

    except Exception as e:
        print(f"Error at index {index}: {e}")

input("Press Enter to exit...")
driver.quit()
