import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os

# Auto-install matching chromedriver
chromedriver_autoinstaller.install()

# Chrome setup
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://inpi.justica.gov.pt/boletim-da-propriedade-industrial")

# Wait for the first .wrapper to load
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
)

# Get first .wrapper div
first_wrapper = driver.find_element(By.CLASS_NAME, "wrapper")

# Find the <a> inside it
link = first_wrapper.find_element(By.TAG_NAME, "a")

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
time.sleep(1)

# Get the actual PDF URL
pdf_url = link.get_attribute("href")
print("PDF URL:", pdf_url)

# Generate filename from link text
bulletin_title = link.text.strip().replace(" ", "_").replace(":", "-")
filename = f"{bulletin_title}.pdf"

# Download the PDF into current script directory
print("Downloading PDF...")
response = requests.get(pdf_url)
with open(filename, "wb") as f:
    f.write(response.content)
print(f"✅ PDF downloaded as: {filename}")

# Optional: Open PDF in new tab
link.click()
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])

# Wait for new tab content
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

print("New tab title:", driver.title)
time.sleep(5)
driver.quit()
