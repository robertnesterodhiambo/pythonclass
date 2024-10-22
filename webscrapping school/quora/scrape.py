import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    
    # Sleep to allow time to view the page (you can adjust this time)
    sleep(5)

# Close the browser after processing
driver.quit()
