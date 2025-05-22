import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

# Step 5: Setup
wait = WebDriverWait(driver, 15)

# The fixed dropdown options
fixed_entries = [
    "Torrance, CA",
    "Tualatin, OR",
    "Fort Pierce, FL",
    "United Kingdom"
]

try:
    # Click the dropdown to activate it
    dropdown_container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-container")))
    dropdown_container.click()
    time.sleep(0.5)

    input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "chosen-search-input")))

    for entry in fixed_entries:
        # Clear and type the entry
        input_box.clear()
        input_box.send_keys(entry)
        time.sleep(0.7)

        # Wait for dropdown items to appear
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.chosen-results li.active-result")))

        found = False
        for item in results:
            if item.text.strip().lower() == entry.lower():
                print("Selected:", item.text)
                item.click()
                found = True
                break

        if not found:
            print(f"Could not find option: {entry}")

        time.sleep(1)

        # Reopen dropdown for next round
        dropdown_container = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".chosen-container")))
        dropdown_container.click()
        input_box = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "chosen-search-input")))

except Exception as e:
    print("Error during dropdown automation:", e)

input("Press Enter to close browser...")
driver.quit()
