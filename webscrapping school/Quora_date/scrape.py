import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Load the CSV file
df = pd.read_csv('merged_output.csv')

# Extract the first 5 links from the 'edit_link' column
edit_links = df['edit_link'].head(5)

# Set up the Chrome WebDriver
service = Service('./chromedriver')  # Adjust path if needed
driver = webdriver.Chrome(service=service)

# Open each link in the browser
try:
    for link in edit_links:
        print(f"Opening: {link}")
        driver.get(link)
        time.sleep(3)  # Pause to let the page load, adjust as needed
finally:
    driver.quit()  # Close the browser after processing
