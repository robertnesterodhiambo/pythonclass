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

# Open the specified URL
driver.get("https://www.agedcarequickstart.com.au/")

# Wait for the input field with ID 'location' to become visible
try:
    location_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "location"))
    )
    
    # Loop through the addresses from 5000 to 5005
    for address in range(5000, 5006):
        # Clear any pre-existing text in the input field
        location_input.clear()
        
        # Enter the address
        location_input.send_keys(str(address))
        
        # Simulate pressing Enter to perform the search
        location_input.send_keys(Keys.RETURN)
        
        # Wait for the page to load results (adjust the sleep time if necessary)
        time.sleep(3)
        
        # You can add code here to process the search results, if needed
        print(f"Searched for address: {address}")
        
        # Optionally capture or process results here

finally:
    # Close the browser
    driver.quit()
