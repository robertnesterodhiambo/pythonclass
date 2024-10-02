from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time  # Import the time module to add a delay
from selenium.webdriver.common.by import By  # Import By for locating elements
from selenium.webdriver.common.action_chains import ActionChains  # Import ActionChains for scrolling

# Set options for Firefox
options = Options()
# options.add_argument('--headless')  # Uncomment to run in headless mode (without opening a browser window)
options.add_argument('--disable-gpu')

# Set the path to the GeckoDriver executable
gecko_driver_path = './geckodriver'  # Assuming the GeckoDriver is in the same folder

# Initialize the Firefox driver with GeckoDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Open the specified URL
url = 'https://ted.europa.eu/en/search/result?notice-type=can-standard%2Ccan-social%2Ccan-desg%2Ccan-tran&place-of-performance=DEU&search-scope=ACTIVE'
driver.get(url)

# Wait for the page to load (you can adjust the sleep time as needed)
time.sleep(5)

# Scroll to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Wait for additional content to load after scrolling
time.sleep(5)  # Adjust this wait time based on how long it takes to load more content

# Locate all <a> tags with the specified class
links_elements = driver.find_elements(By.CSS_SELECTOR, 'a.css-q5fadx.ed8fupw0')

# Extract the href attributes and store them in a list
links = [element.get_attribute('href') for element in links_elements]

# Print the collected links
print("Collected links:")
for link in links:
    print(link)

# Close the browser after use
driver.quit()
