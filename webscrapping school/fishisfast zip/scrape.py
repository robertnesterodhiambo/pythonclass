import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Load CSV and select first 5 rows
csv_path = '100 Country list 20180621.csv'
df = pd.read_csv(csv_path)
entries = df[['countryname', 'city', 'zipcode']].dropna().head(5)

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")

# Launch browser
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")
time.sleep(5)  # Allow full load

# Loop through each entry
for index, row in entries.iterrows():
    try:
        country = row['countryname']
        city = row['city']
        zipcode = str(row['zipcode'])

        # Select and input country
        country_input = driver.find_element(By.ID, "react-select-country-input")
        country_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        time.sleep(0.5)
        country_input.send_keys(country)
        time.sleep(1)
        country_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # Move to next input field
        country_input.send_keys(Keys.TAB)
        time.sleep(1)

        # Get the focused input field
        active_input = driver.switch_to.active_element

        # Scan form labels to determine field type
        form = driver.find_element(By.TAG_NAME, "form")
        labels = form.find_elements(By.CLASS_NAME, "form-label")
        label_texts = [label.text.lower() for label in labels]

        field_type = None
        if any("city" in text for text in label_texts):
            field_type = "city"
        elif any("postal code" in text or "zip" in text for text in label_texts):
            field_type = "zipcode"

        # Enter the appropriate value and press ENTER
        if field_type == "city":
            active_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            active_input.send_keys(city)
            time.sleep(0.5)
            active_input.send_keys(Keys.ENTER)
            print(f"Entered City: {city}")

        elif field_type == "zipcode":
            active_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            active_input.send_keys(zipcode)
            time.sleep(0.5)
            active_input.send_keys(Keys.ENTER)
            print(f"Entered Zip Code: {zipcode}")

        else:
            print("Could not determine input type from labels.")

        time.sleep(2)

    except Exception as e:
        print(f"Error on row {index}: {e}")

input("Press Enter to close the browser...")
driver.quit()
