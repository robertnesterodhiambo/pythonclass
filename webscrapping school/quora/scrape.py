import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Load the CSV file (output.csv)
file_path = 'output.csv'

# Load the data
data = pd.read_csv(file_path)

# Extract the first 5 rows from the "Link" column
links = data['Link'].head(5)

# Set up Chrome WebDriver
chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver')  # Assuming chromedriver is in the same folder
service = Service(chrome_driver_path)

# Initialize the Chrome WebDriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Loop through the first 5 links
for link in links:
    modified_link = link + '/log'  # Append /log to the link
    driver.get(modified_link)  # Open the modified link
    print(f"Opened: {modified_link}")  # Print the modified link
    
    # Scroll to the bottom of the page dynamically
    last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial height

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the presence of the div with class 'q-box'
        try:
            # Wait dynamically until the 'q-box' element appears
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'q-box'))
            )
            print("q-box element appeared, moving to the next page...")
            break  # Exit the loop when the element appears
        except:
            # If no element appears within the wait time, continue scrolling
            print("q-box not found yet, scrolling again...")

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # If no new height, break the loop
            print("Reached the bottom of the page without finding q-box")
            break
        last_height = new_height  # Update last height

# Close the browser after processing
driver.quit()
