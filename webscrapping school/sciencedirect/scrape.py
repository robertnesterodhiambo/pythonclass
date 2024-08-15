from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
url = "https://www.sciencedirect.com/science/article/pii/S0010938X24005286"
driver.get(url)



# Wait for manual interaction
print("Please manually handle the cookies consent and any popups.")
time.sleep(60)  # Keeps the browser open for 60 seconds for manual interaction

# Add any additional operations you want to perform here

# Close the browser
driver.quit()
