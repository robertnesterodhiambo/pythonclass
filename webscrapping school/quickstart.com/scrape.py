from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set the options for headless mode (if needed)
options = Options()
# Uncomment the following line to run in headless mode
# options.add_argument('--headless')

# Specify the path to GeckoDriver
service = Service(executable_path='./geckodriver')

# Initialize the WebDriver with the specified options and service
driver = webdriver.Firefox(service=service, options=options)

# Open the specified URL
driver.get("https://www.agedcarequickstart.com.au/")

# Do your scraping tasks here, e.g., print the page title
print(driver.title)

# Close the browser
driver.quit()
