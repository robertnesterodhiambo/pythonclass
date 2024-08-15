import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Load the Excel file
file_path = "data_final.xlsx"
df = pd.read_excel(file_path)

# Initialize the Firefox WebDriver
service = Service(executable_path="./geckodriver")  # Assuming geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

try:
    # Open the first 5 links from the 'Link' column
    for i, link in enumerate(df['Link'].head(5)):
        driver.get(link)
        time.sleep(3)  # Pause for 3 seconds to let the page load
        
        # Locate the div with id="author-group"
        author_group_div = driver.find_element(By.ID, "author-group")
        
        # Find all buttons within the div with the specified classes
        buttons = author_group_div.find_elements(By.CSS_SELECTOR, ".button-link.button-link-secondary.button-link-underline")
        
        # Click each button
        for button in buttons:
            button.click()
            time.sleep(1)  # Pause to allow any action from the button click to complete
            
finally:
    # Close the browser after opening the links
    driver.quit()
