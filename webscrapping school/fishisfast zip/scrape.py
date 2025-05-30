import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load CSV
csv_path = os.path.join(os.path.dirname(__file__), "100 Country list 20180621.csv")
try:
    df = pd.read_csv(csv_path)
    data_rows = df[['countryname', 'city']].dropna().head(5)
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # Uncomment if you don't need GUI
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Set up ChromeDriver
service = Service("/usr/lib/chromium-browser/chromedriver")  # Adjust if needed
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")

# Wait until the country input is interactable
wait = WebDriverWait(driver, 15)

for index, row in data_rows.iterrows():
    country = row['countryname']
    city = row['city']
    print(f"Processing: {country}, {city}")

    try:
        # Wait for and focus country input (React select)
        country_input = wait.until(EC.presence_of_element_located((By.ID, "react-select-country-input")))
        country_input.click()
        time.sleep(0.3)

        # Type country letter by letter
        for letter in country:
            country_input.send_keys(letter)
            time.sleep(0.1)

        time.sleep(1.0)  # Allow React suggestions to show

        # Dismiss dropdown if present (press ESC)
        country_input.send_keys(Keys.ESCAPE)
        time.sleep(0.3)

        # Clear the input
        country_input.send_keys(Keys.CONTROL + "a")
        country_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

        # Find city input by XPath
        city_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='city']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", city_input)  # Scroll to the input
        city_input.click()
        city_input.clear()

        # Type city letter by letter
        for letter in str(city):
            city_input.send_keys(letter)
            time.sleep(0.1)

        time.sleep(1.5)

        # Clear city input
        city_input.send_keys(Keys.CONTROL + "a")
        city_input.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

    except Exception as e:
        print(f"Error at row {index}: {e}")

print("Finished processing.")
input("Press Enter to exit...")
driver.quit()
