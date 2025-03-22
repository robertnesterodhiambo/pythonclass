from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os

# Set up Firefox options
options = Options()
options.add_argument("--start-maximized")  # Open browser in maximized mode (optional)

# Set up geckodriver path (assuming it's in the same folder as the script)
gecko_path = os.path.join(os.getcwd(), "geckodriver")
service = Service(gecko_path)

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Open the given website
driver.get("https://seaweb.seacoglobal.com/sap/bc/ui5_ui5/sap/zseaco_ue17/index.html")

# Keep the browser open (optional)
input("Press Enter to close the browser...")

driver.quit()
