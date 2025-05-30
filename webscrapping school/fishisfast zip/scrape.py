import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Load CSV and get first 5 countries
csv_path = '100 Country list 20180621.csv'
df = pd.read_csv(csv_path)
countries = df['countryname'].dropna().tolist()[:5]

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Launch Chrome browser
driver = webdriver.Chrome(options=options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")

# Wait for page to load
time.sleep(5)

# Loop through the first 5 countries
for country in countries:
    try:
        input_field = driver.find_element(By.ID, "react-select-country-input")

        # Clear any existing input
        input_field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
        time.sleep(0.5)

        # Type country name and press ENTER
        input_field.send_keys(country)
        time.sleep(1)  # Allow suggestions to render (optional)
        input_field.send_keys(Keys.ENTER)

        print(f"Entered country: {country}")
        time.sleep(2)  # Pause before next entry

    except Exception as e:
        print(f"Error with '{country}': {e}")

input("Press Enter to close the browser...")
driver.quit()
