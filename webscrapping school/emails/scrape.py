from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time  # Import the time module to add a delay

# Set options for Firefox
options = Options()
#options.add_argument('--headless')  # Uncomment to run in headless mode (without opening a browser window)
options.add_argument('--disable-gpu')

# Set the path to the GeckoDriver executable
gecko_driver_path = './geckodriver'  # Assuming the GeckoDriver is in the same folder

# Initialize the Firefox driver with GeckoDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Open the specified URL
url = 'https://ted.europa.eu/en/search/result?notice-type=can-standard%2Ccan-social%2Ccan-desg%2Ccan-tran&place-of-performance=DEU&search-scope=ACTIVE'
driver.get(url)

# Print the page title to confirm the page was loaded
print("Page title:", driver.title)

# Wait for 5 seconds
time.sleep(5)

# Close the browser after use
driver.quit()
