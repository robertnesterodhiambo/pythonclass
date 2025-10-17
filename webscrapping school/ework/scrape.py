#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# === SETUP CHROME ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
# options.add_argument("--headless=new")  # Uncomment for headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

# === OPEN PAGE ===
url = "https://oferty.praca.gov.pl/portal/lista-ofert?sortowanie="
print(f"Opening {url}")
driver.get(url)

# === WAIT UNTIL MAIN PAGE LOADS ===
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Main page loaded.")

# === DYNAMICALLY WAIT FOR POPUP AND CLOSE IT ===
popup_closed = False
end_time = time.time() + 30  # up to 30s wait
while time.time() < end_time:
    try:
        popup = driver.find_element(By.CSS_SELECTOR, "div.epraca-dialog-wrapper")
        close_btn = popup.find_element(By.CSS_SELECTOR, "button.close-dialog")
        if close_btn.is_displayed():
            close_btn.click()
            popup_closed = True
            print("✅ Popup closed dynamically.")
            break
    except Exception:
        pass
    time.sleep(0.5)

if not popup_closed:
    print("ℹ️ No popup detected or it auto-closed.")

# === WAIT FOR JOB LINKS TO LOAD ===
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-link")))
links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
print(f"✅ Found {len(links)} job offers.")

# === ITERATE THROUGH EACH JOB LINK ===
for i in range(len(links)):
    # Re-fetch job links after navigation
    links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
    job = links[i]
    job_title = job.text.strip()
    print(f"\n➡️ Opening job {i + 1}/{len(links)}: {job_title or '(no title)'}")

    # Click the job
    driver.execute_script("arguments[0].click();", job)

    # Wait for job detail page
    try:
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//h1 | //div[contains(@class,'oferta')] | //div[contains(@class,'offer-details')]",
                )
            )
        )
        time.sleep(2)
        print("✅ Job detail page loaded successfully.")
    except TimeoutException:
        print("⚠️ Timeout waiting for job details.")
        continue

    # Go back to main list
    driver.back()

    # Wait for list to reload
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-link")))
        print("↩️ Returned to job list.")
    except TimeoutException:
        print("⚠️ Job list did not reload correctly.")
        continue

    # Re-close popup if it reappears
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close-dialog"))
        )
        close_btn.click()
        print("✅ Popup closed again after navigating back.")
    except Exception:
        pass

print("\n✅ Finished processing all job offers.")
driver.quit()
