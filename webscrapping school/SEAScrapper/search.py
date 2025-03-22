import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Load the CSV file
file_path = "combined_data.csv"
df = pd.read_csv(file_path)

# Set up Firefox WebDriver (GeckoDriver is in the same folder)
gecko_path = "./geckodriver"  # Adjust if needed
service = Service(gecko_path)
options = Options()
options.add_argument("--headless")  # Run in headless mode (optional)

# Start WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Open the target website
url = "https://tex.textainer.com/Equipment/StatusAndSpecificationsInquiry.aspx"
driver.get(url)

print("Website opened successfully!")

# Keep the browser open for interaction (or close it after a delay)
input("Press Enter to exit...")
driver.quit()
