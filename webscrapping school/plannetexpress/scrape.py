import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Load CSV
df = pd.read_csv('100 Country list 20180621.csv')
print(df.head())

# Step 2: Set Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Step 3: Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 4: Navigate to the website
url = "https://planetexpress.com/postage-calculator/"
driver.get(url)

# Step 5: Wait for the dropdown container
wait = WebDriverWait(driver, 15)

try:
    # Click the outer container to activate the input
    dropdown_container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-container")))
    dropdown_container.click()
    time.sleep(0.5)

    # Focus the actual input field
    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "chosen-search-input")))
    driver.execute_script("arguments[0].focus();", input_box)

    print("Cursor is now focused in the input box.")

except Exception as e:
    print(f"Could not focus input box: {e}")

# Pause so user can interact or view
input("Press Enter to close browser...")
driver.quit()
