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

# === Step 2: Setup Selenium Chrome Driver with custom download directory ===
download_dir = os.getcwd()
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

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
        time.sleep(25)
        # === Step 7: Wait for "Download" button by data-testid and click it ===
        download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='side-button']")))
        download_button.click()
        print("Clicked Download button to download converted HTML.")

        # === Step 8: Wait for download to complete ===
        time.sleep(30)  # Adjust based on file size and network speed
        print("Download completed.")

    except Exception as inner_e:
        print("Upload, convert, or download button interaction failed.")
        print("Error details:", inner_e)

except Exception as e:
    print("Automation error:", e)

finally:
    # === Step 9: Close browser ===
    driver.quit()
