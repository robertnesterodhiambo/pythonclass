from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Set the base URL
base_url = 'https://www.zillow.com/'

# Initialize the Firefox WebDriver
service = Service('./geckodriver')  # Assuming 'geckodriver' is in the same directory
driver = webdriver.Firefox(service=service)

# Open the base URL
driver.get(base_url)

# Wait for the input field to be present in the DOM and visible
try:
    input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search']"))
    )

    # Enter the address "Irvine CA 92612"
    input_field.send_keys("Irvine CA 92612")

    # Simulate pressing the 'Enter' key to search
    input_field.send_keys(Keys.RETURN)

    # Wait for the search results to load (you may need to adjust this)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))  # Adjust this to match a real element on the results page
    )
    
    # Wait for 1 minute (60 seconds) to solve CAPTCHA if needed
    time.sleep(60)

finally:
    # Close the browser after use
    driver.quit()
