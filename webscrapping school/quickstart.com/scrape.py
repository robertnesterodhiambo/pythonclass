from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
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

# Initialize a list to hold all links
all_links = []

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
        
        # Select the option with value 50 from the select element with ID 'radius'
        radius_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "radius"))
        )
        select = Select(radius_select)
        select.select_by_value("50")
        
        # Wait for the page to update
        time.sleep(5)
        
        # Scroll to the bottom of the page to load all content
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(3)
            
            # Check new height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Collect all links with the class 'fo-black text-decoration-none'
        anchors = driver.find_elements(By.CSS_SELECTOR, "div.col.mb-4 a.fo-black.text-decoration-none")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if href:
                all_links.append(href)
        
        # Print confirmation for each search
        print(f"Searched for address: {address}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Close the browser
driver.quit()

# Print all collected links
print("Collected links:")
for link in all_links:
    print(link)
