import os
import time
import glob
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Step 0: Install Chromedriver ===
chromedriver_autoinstaller.install()

# === Step 1: Locate the latest Boletim_da_PI_-_YYYY-MM-DD.pdf ===
pdf_pattern = "Boletim_da_PI_-_*.pdf"
pdf_files = glob.glob(pdf_pattern)

if not pdf_files:
    print("No Boletim_da_PI PDF file found in current directory.")
    exit(1)

# Sort by modified time descending to get the latest
pdf_files.sort(key=os.path.getmtime, reverse=True)
latest_pdf = os.path.abspath(pdf_files[0])
print(f"Latest PDF found: {latest_pdf}")

# === Step 2: Setup Selenium Chrome Driver ===
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 30)

try:
    # === Step 3: Navigate to Xodo site ===
    driver.get("https://xodo.com/convert-pdf-to-html")
    
    # === Step 4: Locate hidden input[type=file] and upload ===
    try:
        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        file_input.send_keys(latest_pdf)
        print("File uploaded via input[type='file'].")

        # === Step 5: Wait explicitly for 5 seconds before clicking Convert ===
        time.sleep(5)

        # === Step 6: Wait for "Convert" button to be clickable and click it ===
        convert_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Convert')]")))
        convert_button.click()
        print("Clicked Convert button.")

        # === Step 7: Wait for conversion to complete (adjust time or implement result detection) ===
        time.sleep(60)
        print("Waited for conversion to complete.")

    except Exception as inner_e:
        print("Upload or convert button interaction failed.")
        print("Error details:", inner_e)

except Exception as e:
    print("Automation error:", e)

finally:
    # === Step 8: Close browser ===
    driver.quit()
