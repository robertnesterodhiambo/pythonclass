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

    # Wait for the modal to appear and allow user to log in manually
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-body"))
    )

    # Wait for the user to complete the login manually
    input("Please log in manually, then press Enter to reopen the page...")

    # Reopen the same URL after login is complete
    driver.get("https://www.pesarourbinolavoro.it/curriculum-candidati_1.html")

    # Add any additional actions here if needed after reopening the page

finally:
    # Close the driver after the task is completed
    input("Press Enter to close the browser...")
    driver.quit()
