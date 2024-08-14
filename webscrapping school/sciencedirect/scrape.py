from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set up options to specify the WebDriver location
options = Options()
options.headless = False  # Set to True if you want to run in headless mode (without GUI)

# Define the path to the WebDriver in the same directory as this script
webdriver_path = './geckodriver'  # Adjust according to your OS (e.g., './geckodriver.exe' for Windows)

# Create a WebDriver service
service = Service(executable_path=webdriver_path)

# Initialize the Firefox WebDriver with the specified service
driver = webdriver.Firefox(service=service, options=options)

# Open the desired URL
url = "https://www.sciencedirect.com/search?qs=%22additive%20manufacturing%22&affiliations=Germany"
driver.get(url)

# Add any additional operations you want to perform here
# For example, you can find elements, click buttons, or extract information

# Close the browser after some delay (optional)
import time
time.sleep(10)  # Keeps the browser open for 10 seconds

driver.quit()
