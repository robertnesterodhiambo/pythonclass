#!/usr/bin/env python3
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

# === SETUP CHROME ===
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 30)

url = "https://oferty.praca.gov.pl/portal/lista-ofert?sortowanie="
print(f"Opening {url}")
driver.get(url)

# === Wait for complete page load ===
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("✅ Main page loaded.")


def scroll_to_bottom():
    """Scroll to the bottom dynamically until no more content loads."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("✅ Scrolled to bottom.")


def close_popup_if_present():
    """Close mobile app popup dynamically if it appears."""
    end_time = time.time() + 10
    while time.time() < end_time:
        try:
            popup = driver.find_element(By.CSS_SELECTOR, "div.epraca-dialog-wrapper")
            close_btn = popup.find_element(By.CSS_SELECTOR, "button.close-dialog")
            if close_btn.is_displayed():
                close_btn.click()
                print("✅ Popup closed.")
                return
        except Exception:
            pass
        time.sleep(0.5)


def wait_for_jobs_to_load():
    """Wait for job list to appear after full dynamic load."""
    # Ensure full ready state first
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    scroll_to_bottom()
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-link")))
    time.sleep(1)
    print("✅ Job list fully loaded.")


def process_jobs_on_page():
    """Click each job link, view details, and return."""
    wait_for_jobs_to_load()
    job_links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
    print(f"✅ Found {len(job_links)} job offers on this page.")

    for i in range(len(job_links)):
        try:
            job_links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
            job = job_links[i]
            job_title = job.text.strip() or "(no title)"
            print(f"\n➡️ Opening job {i + 1}/{len(job_links)}: {job_title}")

            driver.execute_script("arguments[0].scrollIntoView(true);", job)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", job)

            # Wait for job detail page
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h1 | //div[contains(@class,'oferta')] | //div[contains(@class,'offer-details')]")
                )
            )
            print("✅ Job details loaded.")
            time.sleep(1)

            driver.back()
            wait_for_jobs_to_load()
            print("↩️ Returned to job list.")
            close_popup_if_present()

        except (TimeoutException, StaleElementReferenceException):
            print("⚠️ Skipped due to timeout or stale element.")
            driver.back()
            wait_for_jobs_to_load()
            continue


def get_total_pages():
    """Wait until page is fully ready, then detect total pages."""
    scroll_to_bottom()
    wait_for_jobs_to_load()
    try:
        page_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
        total_pages = int(page_input.get_attribute("max") or 1)
        print(f"📄 Total pages detected: {total_pages}")
        return total_pages
    except Exception:
        print("⚠️ Could not determine total pages.")
        return 1


def go_to_page(page_number):
    """Switch page dynamically by editing the input field."""
    try:
        page_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
        driver.execute_script("arguments[0].value = '';", page_input)
        page_input.send_keys(str(page_number))
        page_input.send_keys("\n")
        print(f"➡️ Switching to page {page_number}...")

        wait_for_jobs_to_load()
        close_popup_if_present()
        print(f"✅ Page {page_number} loaded successfully.")
    except Exception as e:
        print(f"⚠️ Could not switch to page {page_number}: {e}")


# === MAIN SCRIPT FLOW ===
close_popup_if_present()
total_pages = get_total_pages()

for page in range(1, total_pages + 1):
    print(f"\n=============================\n📄 Processing page {page}/{total_pages}\n=============================")
    process_jobs_on_page()
    if page < total_pages:
        go_to_page(page + 1)

print("\n✅ Finished all pages successfully.")
driver.quit()
