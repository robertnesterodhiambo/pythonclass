import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time

# Automatically install chromedriver
chromedriver_autoinstaller.install()

# Load the wemailweb.csv file
file_path = 'wemailweb.csv'
data = pd.read_csv(file_path)

# Extract the first 5 website domains
first_five_websites = data['websites'].head(30)

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=Service(), options=options)

# Open each website using the WebDriver
for website in first_five_websites:
    url = f"http://{website}"  # Construct the full URL
    try:
        driver.get(url)
        print(f"Opened {url}")
        time.sleep(5)  # Wait for a few seconds to observe the page before moving to the next
    except Exception as e:
        print(f"Failed to open {url}: {e}")

# Close the browser once done
driver.quit()
