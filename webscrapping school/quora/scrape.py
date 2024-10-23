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

# Step 1: Open Quora's homepage
driver.get("https://www.quora.com/")
print("Opened Quora. Please log in...")

# Step 2: Wait for the user to log in manually
input("Press Enter after logging in...")  # Wait for user confirmation after logging in

# Step 3: Loop through the first 5 links from the CSV file
for link in links:
    modified_link = link + '/log'  # Append /log to the link
    try:
        driver.get(modified_link)  # Open the modified link
        print(f"Opened: {modified_link}")  # Print the modified link
        
        # Wait for the first 'q-box' to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'q-box'))
        )
        print("First q-box element found, starting infinite scroll...")
        
        # Start scrolling to load more content
        last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial height

        while True:
            # Scroll down to the bottom of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            sleep(2)
            
            # Check for more 'q-box' elements being loaded
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'q-box'))
                )
                print("More q-box elements loaded...")
            except:
                print("No new q-box elements found after scroll...")
            
            # Calculate new scroll height and compare with last height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # If no new height, break the loop
                print("Reached the bottom of the page, no more content to load")
                break
            last_height = new_height  # Update last height
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Close the browser after processing
driver.quit()
