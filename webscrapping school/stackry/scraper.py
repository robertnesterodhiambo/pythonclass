import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Read the CSV file and get the first 5 rows
df = pd.read_csv('100 Country list 20180621.csv')  # Ensure correct file path
rows = df[['countryname', 'city', 'zipcode']].head(5)  # Extract only needed columns

# Set up the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Navigate to the Stackry shipping calculator page
    driver.get("https://www.stackry.com/shipping-calculator")

    # Wait until the iframe is present and switch to it
    iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myIframe")))
    driver.switch_to.frame(iframe)

    for _, row in rows.iterrows():
        country = row['countryname']
        city = str(row['city']) if not pd.isna(row['city']) else ""
        zipcode = str(row['zipcode']) if not pd.isna(row['zipcode']) else ""

        # Wait for the country input field
        country_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-select-4-input"))
        )
        country_input.clear()
        country_input.send_keys(country)
        time.sleep(1)
        country_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Try to enter city if field appears
        try:
            city_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "shipToCity"))
            )
            city_input.clear()
            city_input.send_keys(city)
            print(f"Entered city: {city}")
        except:
            print("City input not present.")

        # Try to enter zipcode if field appears
        try:
            zip_input = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.ID, "shipToZip"))
            )
            zip_input.clear()
            zip_input.send_keys(zipcode)
            print(f"Entered zipcode: {zipcode}")
        except:
            print("Zipcode input not present.")

        # Wait a bit before next iteration
        time.sleep(2)

finally:
    time.sleep(5)
    driver.quit()
