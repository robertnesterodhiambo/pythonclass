import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time

# Automatically install chromedriver
chromedriver_autoinstaller.install()

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument('--headless')  # Optional: Run in headless mode (no GUI)
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the target URL
driver.get("https://whoer.net/checkwhois")

# Load the CSV file
df = pd.read_csv('wemailweb.csv')

# Filter out rows with NaN in the 'websites' column
valid_websites = df['websites'].dropna()

# List to store the ISP data
isp_data = []

# Loop through the first 5 valid websites
for website in valid_websites.head(5):
    # Find the input field by ID and enter the website
    input_field = driver.find_element(By.ID, "host")
    input_field.clear()  # Clear the input field
    input_field.send_keys(website)  # Enter the website

    # Simulate pressing Enter
    input_field.send_keys(Keys.RETURN)

    # Wait for the results to load (adjust as necessary)
    time.sleep(5)  # Wait time for results to load

    # Collect the ISP information
    try:
        # Wait until the ISP span appears in the page
        isp_element = driver.find_element(By.CSS_SELECTOR, "span.ico-holder.ico-isp")
        isp_text = isp_element.text  # Get the ISP text
    except Exception as e:
        isp_text = "N/A"  # If not found, set to 'N/A'

    # Append the ISP data to the list
    isp_data.append(isp_text)

    # Navigate back to the original page to enter the next website
    driver.get("https://whoer.net/checkwhois")

# Close the WebDriver
driver.quit()

# Add the ISP data as a new column to the original DataFrame
df['ISP'] = pd.Series(isp_data)

# Save the updated DataFrame to a new CSV file
df.to_csv('wemailweb_with_isp.csv', index=False)

print("Data has been collected and saved to 'wemailweb_with_isp.csv'.")
