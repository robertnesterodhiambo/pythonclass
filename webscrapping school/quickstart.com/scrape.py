from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
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

# Loop through the addresses from 1000 to 1005
for address in range(1000, 1006):
    # Find the input field by its ID
    location_input = driver.find_element(By.ID, "location")
    
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
    
    # You can add code to capture or process results here
    
# Close the browser
driver.quit()
