import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time

# Load the Excel file
file_path = "data_final.xlsx"
df = pd.read_excel(file_path)

# Initialize the Firefox WebDriver
service = Service(executable_path="./geckodriver")  # Assuming geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Open the first 5 links from the 'Link' column
for i, link in enumerate(df['Link'].head(5)):
    driver.get(link)
    time.sleep(3)  # Pause for 3 seconds to let the page load

# Close the browser after opening the links
driver.quit()
