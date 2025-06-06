import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Step 1: Load the CSV
csv_file = "100 Country list 20180621.csv"
df = pd.read_csv(csv_file)
print(df.head())  # Optional: preview data

# Step 2: Open the Shipito shipping calculator using Selenium

# Configure Selenium to run Chrome in headless mode (optional)
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment for headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)  # You can add executable_path if needed

# Open the shipping calculator page
url = "https://www.shipito.com/en/shipping-calculator"
driver.get(url)

# Optional: wait for the page to load
time.sleep(5)

print("Shipito shipping calculator page opened.")

# Don’t forget to close the browser when done
# driver.quit()
