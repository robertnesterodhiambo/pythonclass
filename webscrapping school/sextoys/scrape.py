import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

# Path to the geckodriver executable
geckodriver_path = './geckodriver'

# Load the Excel file
file_path = 'navigation_links.xlsx'
df = pd.read_excel(file_path)

# Ensure the 'link' column exists in the DataFrame
if 'link' not in df.columns:
    raise ValueError("The DataFrame does not contain a 'link' column.")

# Set up Firefox WebDriver
options = Options()
options.headless = False  # Set to True if you don't need a visible browser window
service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Open each link from the DataFrame
for index, row in df.iterrows():
    link = row['link']
    print(f"Opening link: {link}")
    driver.get(link)
    time.sleep(5)  # Wait for 5 seconds to ensure the page loads completely

# Close the WebDriver
driver.quit()
