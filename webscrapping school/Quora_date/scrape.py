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

try:
    # Step 1: Open Quora for login
    print("Opening Quora for login...")
    driver.get('https://www.quora.com/')
    
    # Wait for the user to log in
    input("Press Enter after logging in to Quora...")
    
    # Step 2: Open each link from the CSV
    for link in edit_links:
        print(f"Opening: {link}")
        driver.get(link)
        time.sleep(3)  # Pause to let the page load, adjust as needed

finally:
    # Close the browser after processing
    driver.quit()
