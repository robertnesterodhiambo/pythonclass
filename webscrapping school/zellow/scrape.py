from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# Set the base URL
base_url = 'https://www.zillow.com/'

# Initialize the Firefox WebDriver
service = Service('./geckodriver')  # Assuming 'geckodriver' is in the same directory
driver = webdriver.Firefox(service=service)

# Open the base URL
driver.get(base_url)

# You can add more actions here if needed

# Close the browser after use
# driver.quit()
