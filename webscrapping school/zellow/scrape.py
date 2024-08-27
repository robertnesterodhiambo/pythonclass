from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# Set the base URL
base_url = 'https://www.zillow.com/'

# Initialize the Firefox WebDriver
service = Service('./geckodriver')  # Assuming 'geckodriver' is in the same directory
driver = webdriver.Firefox(service=service)

# Open the base URL
driver.get(base_url)

# Wait for the input field to be present in the DOM and visible
try:
    input_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search']"))
    )

    # Enter the address "Irvine CA 92612"
    input_field.send_keys("Irvine CA 92612")

    # Simulate pressing the 'Enter' key to search
    input_field.send_keys(Keys.RETURN)

    # Wait for the "Press & Hold" CAPTCHA to appear
    press_hold_p = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//p[text()='Press & Hold']"))
    )

    # Assuming the CAPTCHA button is the next sibling of the <p> tag
    press_hold_button = press_hold_p.find_element(By.XPATH, "./following-sibling::button")

    # Simulate the click and hold action
    action = ActionChains(driver)
    action.click_and_hold(press_hold_button).perform()

    # Wait until the CAPTCHA is resolved and search results are displayed
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))  # Adjust this to match a real element on the results page
    )

finally:
    # Close the browser after use
    driver.quit()
