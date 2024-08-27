import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# Load the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Set up the Firefox WebDriver (GeckoDriver)
service = Service('./geckodriver')  # Ensure the geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Get the first link from the DataFrame
first_link = df.loc[0, 'Link']
print(f"Opening the first link: {first_link}")

# Open the first link in the browser
driver.get(first_link)

# Wait for a few seconds (adjust as needed)
driver.implicitly_wait(10)  # Adjust the wait time based on your needs

# Close the browser
driver.quit()
