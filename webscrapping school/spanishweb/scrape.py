from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to geckodriver
service = Service('./geckodriver')  # Ensure geckodriver is in the same folder as this script

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(service=service)

# Open the desired URL
driver.get("https://www.pesarourbinolavoro.it/curriculum-candidati_1.html")

# Wait for the "ACCEDI" button to be clickable and then click it
try:
    accedi_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-warning"))
    )
    accedi_button.click()

    # Wait for any modal or login section to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "modalLogin"))  # Adjust this to the correct locator of the modal
    )

    # Add any additional actions you want to perform here

finally:
    # Close the driver after your task
    driver.quit()
