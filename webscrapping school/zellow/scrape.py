from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

# Set up the Firefox options (optional)
options = Options()
options.headless = False  # Set to True if you want to run in headless mode (no browser UI)

# Specify the path to the GeckoDriver (assuming it's in the same folder as this script)
service = FirefoxService(executable_path='./geckodriver')

# Create a new Firefox WebDriver instance
driver = webdriver.Firefox(service=service, options=options)

# Open the Zillow website
driver.get('https://www.zillow.com/')

# The browser will remain open until you close it
# You can add further code here to interact with the page

# Close the browser after 10 seconds (or whenever you are done)
import time
time.sleep(10)
driver.quit()
