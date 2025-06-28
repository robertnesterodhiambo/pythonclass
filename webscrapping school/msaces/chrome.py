import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time

# Step 1: Auto-install chromedriver that matches your Chrome
chromedriver_autoinstaller.install()

# Step 2: Get current folder and load first .xlsx file
current_folder = os.path.dirname(os.path.abspath(__file__))
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx')]

if not xlsx_files:
    print("No .xlsx file found in the folder.")
    exit()

xlsx_path = os.path.join(current_folder, xlsx_files[0])
print(f"Reading Excel file: {xlsx_files[0]}")
df = pd.read_excel(xlsx_path)
print(df.head())

# Step 3: Set up Selenium Chrome
options = Options()
options.add_argument("--start-maximized")  # Optional
# options.add_argument("--headless")  # Uncomment if you want headless mode

driver = webdriver.Chrome(options=options)

# Step 4: Open the website
url = "https://www.racius.com/"
driver.get(url)

# Optional: Wait to see the browser open before it closes
time.sleep(5)

# driver.quit()  # Uncomment this if you want to close the browser after 5 seconds
