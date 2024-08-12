from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Set the options for headless mode (optional)
options = Options()
# Uncomment the following line to run in headless mode
# options.add_argument('--headless')

# Specify the path to GeckoDriver
service = Service(executable_path='./geckodriver')

# Initialize the WebDriver with the specified options and service
driver = webdriver.Firefox(service=service, options=options)

# The URL to be loaded
url = "https://www.agedcarequickstart.com.au/"

# Loop through the addresses from 5000 to 5005
for address in range(5000, 5006):
    # Load the default URL before each search
    driver.get(url)
    
    try:
        # Wait for the input field with ID 'location' to become visible
        location_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "location"))
        )
        
        # Clear any pre-existing text in the input field
        location_input.clear()
        
        # Enter the address
        location_input.send_keys(str(address))
        
        # Wait for a short moment to simulate user typing
        time.sleep(1)
        
        # Simulate pressing Enter to perform the search
        location_input.send_keys(Keys.RETURN)
        
        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'results')]"))  # Replace with the actual results container element
        )
        
        # Wait for a moment to ensure results are fully loaded
        time.sleep(3)
        
        # Print confirmation for each search
        print(f"Searched for address: {address}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Close the browser
driver.quit()
