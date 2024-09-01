from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time  # Import time module to use sleep function

# Create a service object and specify the geckodriver path
service = Service('./geckodriver')  # './geckodriver' assumes geckodriver is in the same folder as this script

# Create a new instance of Firefox WebDriver
driver = webdriver.Firefox(service=service)

# Open the specified URL
driver.get('https://adasat.online/kw-en/product-list&types=&brand=&color=&collections=&replacement_list_id=&star_list_id=&sortby=4')

# Wait for 5 seconds
time.sleep(5)

# Close the browser
driver.quit()
