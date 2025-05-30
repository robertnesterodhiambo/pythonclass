import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Load the CSV and select the first 5 entries
csv_path = '100 Country list 20180621.csv'
df = pd.read_csv(csv_path)
entries = df[['countryname', 'city', 'zipcode']].dropna().head(5)

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")

# Launch browser
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")
time.sleep(5)  # Wait for the page to load

# Process each entry
for index, row in entries.iterrows():
    try:
        country = row['countryname']
        city = row['city']
        zipcode = str(row['zipcode'])

        # Enter country
        country_input = driver.find_element(By.ID, "react-select-country-input")
        country_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        time.sleep(0.5)
        country_input.send_keys(country)
        time.sleep(1)
        country_input.send_keys(Keys.ENTER)
        time.sleep(1)

        # Move to next field (City or Postal Code)
        country_input.send_keys(Keys.TAB)
        time.sleep(1)

        active_input = driver.switch_to.active_element

        # Scan form labels to determine if it's City or Postal Code
        form = driver.find_element(By.TAG_NAME, "form")
        labels = form.find_elements(By.CLASS_NAME, "form-label")
        label_texts = [label.text.lower() for label in labels]

        # Determine field type
        field_type = None
        if any("city" in text for text in label_texts):
            field_type = "city"
        elif any("postal code" in text or "zip" in text for text in label_texts):
            field_type = "zipcode"

        # Enter city and press ENTER, or enter postal code and just TAB three times
        if field_type == "city":
            active_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            active_input.send_keys(city)
            time.sleep(0.5)
            active_input.send_keys(Keys.ENTER)
            print(f"Entered City: {city}")
            # Move to the next input point (TAB three times to the "weight" input field)
            active_input.send_keys(Keys.TAB)
            time.sleep(0.5)
            active_input.send_keys(Keys.TAB)
            time.sleep(0.5)
            active_input.send_keys(Keys.TAB)

        elif field_type == "zipcode":
            active_input.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
            active_input.send_keys(zipcode)
            time.sleep(0.5)
            # Move to the next input point (TAB three times to the "weight" input field) without pressing ENTER
            active_input.send_keys(Keys.TAB)
            time.sleep(0.5)
            active_input.send_keys(Keys.TAB)
            time.sleep(0.5)
            active_input.send_keys(Keys.TAB)
            print(f"Entered Zip Code: {zipcode}")

        else:
            print("Could not determine input type from labels.")

        # Focus on the "weight" input field after 3 tabs
        weight_input = driver.find_element(By.NAME, "weight")
        weight_input.click()
        time.sleep(1)

        time.sleep(2)

    except Exception as e:
        print(f"Error on row {index}: {e}")

input("Press Enter to close the browser...")
driver.quit()
