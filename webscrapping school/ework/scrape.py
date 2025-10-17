#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# === Target URL ===
URL = "https://oferty.praca.gov.pl/portal/lista-ofert?sortowanie="

# === Chrome setup ===
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless=new")  # Uncomment to run in headless mode

# === Auto-install ChromeDriver ===
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

print(f"Opening {URL}")
driver.get(URL)

# === Wait for full page load ===
try:
    WebDriverWait(driver, 30).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    print("✅ Page HTML fully loaded.")
except TimeoutException:
    print("⚠️ Timeout while waiting for page to fully load.")

# === Wait for job rows to appear ===
try:
    rows = WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.mat-mdc-row"))
    )
    print(f"✅ Found {len(rows)} job rows loaded on the page.")
except TimeoutException:
    print("⚠️ No job rows appeared within timeout.")
    driver.quit()
    exit()

# === Example: Extract first few job postings ===
for i, row in enumerate(rows[:5], start=1):
    try:
        title = row.find_element(By.CSS_SELECTOR, "td.mat-column-stanowisko a").text.strip()
        employer = row.find_element(By.CSS_SELECTOR, "td.mat-column-pracodawca").text.strip()
        location = row.find_element(By.CSS_SELECTOR, "td.mat-column-miejscePracy").text.strip()
        print(f"{i}. {title} | {employer} | {location}")
    except Exception:
        continue

input("\nPress Enter to close browser...")
driver.quit()
