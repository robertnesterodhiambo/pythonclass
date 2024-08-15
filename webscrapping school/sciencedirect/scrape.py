from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

# Set up options for Firefox WebDriver
options = Options()
options.headless = False  # Set to True if you want to run in headless mode (without GUI)

# Define the path to the GeckoDriver in the same directory as this script
geckodriver_path = './geckodriver'  # Adjust if needed

# Create a Firefox WebDriver service
service = Service(executable_path=geckodriver_path)

# Initialize the Firefox WebDriver with the specified service and options
driver = webdriver.Firefox(service=service, options=options)

# Open the desired URL
url = "https://www.sciencedirect.com/"
driver.get(url)

# Locate the input field by ID and enter the search term
search_input = driver.find_element(By.ID, "qs")
search_input.send_keys('"additive manufacturing"')  # Enter the search term with quotes

# Locate and click the search button
search_button = driver.find_element(By.CSS_SELECTOR, ".button.button-primary.button-icon-left")
search_button.click()

# Add any additional operations you want to perform here

# Close the browser after some delay (optional)
time.sleep(10)  # Keeps the browser open for 10 seconds

driver.quit()
