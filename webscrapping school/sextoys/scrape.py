from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Set up the Firefox WebDriver
service = Service('./geckodriver')  # No need to specify path if in the same folder
driver = webdriver.Firefox(service=service)

# Open a website
driver.get('https://example.com')

# Wait for the page to load
time.sleep(3)

# Find an element (e.g., by its tag name, ID, class, etc.)
element = driver.find_element(By.TAG_NAME, 'h1')

# Print the text of the element
print(element.text)

# Close the browser
driver.quit()
