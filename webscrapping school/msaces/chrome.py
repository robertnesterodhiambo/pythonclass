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

# Auto-install ChromeDriver
chromedriver_autoinstaller.install()

# Load first .xlsx file
current_folder = os.path.dirname(os.path.abspath(__file__))
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx')]

if not xlsx_files:
    print("No .xlsx file found.")
    exit()

xlsx_path = os.path.join(current_folder, xlsx_files[0])
df = pd.read_excel(xlsx_path)

# Ensure 'Titular' column exists
if 'Titular' not in df.columns:
    print("Missing 'Titular' column.")
    exit()

titulars = df['Titular'].dropna().astype(str).tolist()[:5]

# Set up Chrome
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Go to main page
driver.get("https://www.racius.com/")

# Begin loop over names
for name in titulars:
    try:
        print(f"\n[SEARCH] {name}")
        
        # Wait for input
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "main-search")))
        search_input.clear()
        search_input.send_keys(name)
        search_input.send_keys(Keys.ENTER)

        # Wait for results div
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
        time.sleep(2)  # Small delay to allow links to fully load

        # Get all result links
        result_links = driver.find_elements(By.CSS_SELECTOR, "div.col--one a.results__col-link")
        print(f"[FOUND] {len(result_links)} links")

        links = [link.get_attribute('href') for link in result_links]

        for i, link in enumerate(links, start=1):
            try:
                print(f"  [OPENING {i}/{len(links)}] {link}")
                driver.get(link)
                time.sleep(3)  # Wait while on company page

                driver.back()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
                time.sleep(1)  # Allow links to reload

            except Exception as e:
                print(f"  [ERROR opening link {i}]: {e}")
        
        # Go back to home for the next search
        driver.get("https://www.racius.com/")
        time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Failed search for '{name}': {e}")

# driver.quit()  # Uncomment to close browser when done
