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

titulars = df['Titular'].dropna().astype(str).tolist()[:5]  # Limit to first 5 for testing

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

        while True:
            # Wait for results
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
            time.sleep(1)

            result_cards = driver.find_elements(By.CSS_SELECTOR, "div.col--one a.results__col-link")
            print(f"  [PAGE] Found {len(result_cards)} results")

            for i in range(len(result_cards)):
                try:
                    # Re-fetch fresh elements to avoid stale reference
                    result_cards = driver.find_elements(By.CSS_SELECTOR, "div.col--one a.results__col-link")
                    result = result_cards[i]

                    name_text = result.text.strip()
                    print(f"  [OPENING {i+1}/{len(result_cards)}] {name_text}")

                    # Scroll into view
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result)
                    time.sleep(1)

                    # Use JS click to avoid interception
                    driver.execute_script("arguments[0].click();", result)

                    # Wait for company page to load
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                    time.sleep(2)

                    # (Optional) Extract company data here...

                    driver.back()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
                    time.sleep(1)

                except Exception as e:
                    print(f"  [ERROR opening result {i+1}]: {e}")
                    # Recover by restarting the search
                    driver.get("https://www.racius.com/")
                    search_input = wait.until(EC.element_to_be_clickable((By.ID, "main-search")))
                    search_input.clear()
                    search_input.send_keys(name)
                    search_input.send_keys(Keys.ENTER)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
                    time.sleep(2)
                    break  # Skip current page if fail

            # Try to click the paginator "Next" button
            try:
                next_li = driver.find_element(By.CSS_SELECTOR, 'li.paginator__nav.btn.btn--round.ml--1')
                next_a = next_li.find_element(By.TAG_NAME, 'a')
                next_href = next_a.get_attribute("href")

                if next_href:
                    print(f"  [→] Next page: {next_href}")
                    driver.get(next_href)
                    time.sleep(2)
                else:
                    print("  [×] Next button inactive. Done with pages.")
                    break
            except:
                print("  [×] No Next button found. Done with pages.")
                break

        # Return to homepage for next titular
        driver.get("https://www.racius.com/")
        time.sleep(2)

    except Exception as e:
        print(f"[ERROR] Problem with '{name}': {e}")

# Done
driver.quit()
