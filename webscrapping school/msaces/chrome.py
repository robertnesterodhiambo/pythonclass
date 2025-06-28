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

# Load Excel file
current_folder = os.path.dirname(os.path.abspath(__file__))
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx')]

if not xlsx_files:
    print("No .xlsx file found.")
    exit()

xlsx_path = os.path.join(current_folder, xlsx_files[0])
df = pd.read_excel(xlsx_path)

if 'Titular' not in df.columns:
    print("Missing 'Titular' column.")
    exit()

titulars = df['Titular'].dropna().astype(str).tolist()[:5]

# Set up Selenium
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.racius.com/")

# Loop through each Titular
for name in titulars:
    try:
        print(f"\n[SEARCHING] {name}")
        
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "main-search")))
        search_input.clear()
        search_input.send_keys(name)
        search_input.send_keys(Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
        time.sleep(2)

        # Scroll until no new results load
        print("[SCROLLING] Loading all search results...")
        last_count = 0
        scroll_attempts = 0
        max_scroll_attempts = 1  # Prevent infinite scroll

        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            results = driver.find_elements(By.CSS_SELECTOR, "div.col--one a.results__col-link")
            if len(results) > last_count:
                last_count = len(results)
                scroll_attempts = 0  # Reset if more results appear
            else:
                scroll_attempts += 1

        print(f"[FOUND] {last_count} links")

        # Collect links
        links = [link.get_attribute('href') for link in results]

        for i, link in enumerate(links, start=1):
            try:
                print(f"  [OPENING {i}/{len(links)}] {link}")
                driver.get(link)
                time.sleep(3)

                driver.back()
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
                time.sleep(1)

            except Exception as e:
                print(f"  [ERROR opening link {i}]: {e}")

        driver.get("https://www.racius.com/")
        time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Problem with '{name}': {e}")

# driver.quit()
