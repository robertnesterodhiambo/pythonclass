import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

# Step 1: Auto-install chromedriver
chromedriver_autoinstaller.install()

# Step 2: Read the first .xlsx file
current_folder = os.path.dirname(os.path.abspath(__file__))
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx')]

if not xlsx_files:
    print("No .xlsx file found in the folder.")
    exit()

xlsx_path = os.path.join(current_folder, xlsx_files[0])
df = pd.read_excel(xlsx_path)

# Check for 'Titular' column
if 'Titular' not in df.columns:
    print("The 'Titular' column was not found in the Excel file.")
    exit()

titulars = df['Titular'].dropna().astype(str).tolist()[:5]

# Step 3: Set up Selenium
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment for headless mode

driver = webdriver.Chrome(options=options)

# Step 4: Visit racius.com
driver.get("https://www.racius.com/")

wait = WebDriverWait(driver, 30)

# Step 5: Interact with search
for name in titulars:
    try:
        # Wait for search input
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "main-search")))

        # Clear and type name
        search_input.clear()
        search_input.send_keys(name)
        search_input.send_keys(Keys.ENTER)

        print(f"[INFO] Searched: {name}")

        # Wait for results to load (you can adjust this condition to something smarter if needed)
        time.sleep(4)  # or wait for a result element

        # Optionally, go back to home to reset everything
        driver.get("https://www.racius.com/")
        time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Failed on '{name}': {e}")

# Uncomment to close the browser after done
# driver.quit()
