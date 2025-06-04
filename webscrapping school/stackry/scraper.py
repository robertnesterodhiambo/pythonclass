import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Read the CSV file and get the first 5 country names
df = pd.read_csv('100 Country list 20180621.csv')  # Adjust the path if needed
countries = df['countryname'].head(5)  # Assuming 'countryname' is the name of the column

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Navigate to the Stackry shipping calculator page
    driver.get("https://www.stackry.com/shipping-calculator")

    # Wait until the iframe is present and switch to it
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame(iframe)

    for country in countries:
        # Wait until the country input field is present inside the iframe
        country_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "react-select-4-input")))

        # Clear the input field if needed (sometimes previous values persist)
        country_input.clear()

        # Enter the country name into the input field
        country_input.send_keys(country)
        time.sleep(1)  # Wait for the dropdown options to load

        # Press Enter to select the typed country (trigger dropdown selection)
        country_input.send_keys(Keys.RETURN)
        time.sleep(2)  # Wait for the dropdown to process and select the country

        # Optional: Print out the selected country for verification
        print(f"Selected Country: {country}")

        # Wait before proceeding to the next country
        time.sleep(2)

finally:
    # Keep the browser open for a short duration to observe
    time.sleep(5)
    driver.quit()  # Close the browser
