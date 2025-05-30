import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Setup file path and read CSV
csv_path = os.path.join(os.path.dirname(__file__), "100 Country list 20180621.csv")

# Load the CSV into a DataFrame
try:
    df = pd.read_csv(csv_path)
    country_names = df['countryname'].dropna().tolist()[:5]  # First 5 country names
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--headless")  # Uncomment if you want headless mode
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Setup driver service
service = Service("/usr/lib/chromium-browser/chromedriver")  # Adjust if needed

# Launch browser
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.fishisfast.com/en/shipping_calculator")

# Wait for page to load
time.sleep(5)

# Loop through the first 5 countries
for country in country_names:
    print(f"Typing country: {country}")
    try:
        input_elem = driver.find_element(By.ID, "react-select-country-input")
        input_elem.click()
        time.sleep(0.5)

        # Type the country name letter by letter
        for letter in country:
            input_elem.send_keys(letter)
            time.sleep(0.1)  # Delay between keystrokes

        time.sleep(1)  # Wait for dropdown suggestion (if needed)

        # Clear input: send BACKSPACE repeatedly or Ctrl+A + Delete
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)

    except Exception as e:
        print(f"Error processing '{country}': {e}")

# Done
print("Done typing countries.")
input("Press Enter to close browser...")
driver.quit()
