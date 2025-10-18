#!/usr/bin/env python3
import time
import csv
import os
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

wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
print("✅ Main page loaded.")

# === CSV SETUP ===
csv_file = "job_titles.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["jobtitle"])  # header


def save_job_title(title):
    """Save job title immediately to CSV."""
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([title])
    print(f"💾 Saved job title: {title}")


def close_popup_initially():
    """Wait up to 2 minutes for the popup (only once, at start)."""
    print("⏳ Waiting for potential popup (max 2 minutes)...")
    end_time = time.time() + 120
    while time.time() < end_time:
        try:
            popup = driver.find_element(By.CSS_SELECTOR, "div.epraca-dialog-wrapper")
            close_btn = popup.find_element(By.CSS_SELECTOR, "button.close-dialog")
            if close_btn.is_displayed():
                driver.execute_script("arguments[0].click();", close_btn)
                print("✅ Popup closed.")
                return
        except Exception:
            pass
        time.sleep(1)
    print("⚠️ No popup appeared within 2 minutes.")


def wait_for_jobs_to_load():
    """Ensure full page and job list are ready."""
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-link")))
        time.sleep(1)
        print("✅ Job list loaded.")
    except TimeoutException:
        print("⚠️ Job list did not fully load.")


def process_jobs_on_page():
    """Click each job link, wait 5s, collect title, then return."""
    wait_for_jobs_to_load()
    job_links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
    print(f"✅ Found {len(job_links)} job offers on this page.")

    for i in range(len(job_links)):
        try:
            job_links = driver.find_elements(By.CSS_SELECTOR, "a.icon-link")
            job = job_links[i]
            job_title_text = job.text.strip() or "(no title)"
            print(f"\n➡️ Opening job {i + 1}/{len(job_links)}: {job_title_text}")

            driver.execute_script("arguments[0].scrollIntoView(true);", job)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", job)

            # Wait for page to fully load
            time.sleep(5)

            # Extract breadcrumb job title
            try:
                label = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "label.xng-breadcrumb-trail"))
                )
                label_text = label.text.strip()
                save_job_title(label_text)
            except Exception:
                print("⚠️ Could not find job title label after 5 seconds.")
                save_job_title("(missing title)")

            driver.back()
            wait_for_jobs_to_load()

        except (TimeoutException, StaleElementReferenceException):
            print("⚠️ Skipped due to timeout or stale element.")
            driver.back()
            wait_for_jobs_to_load()
            continue


def get_total_pages():
    """Wait for full page load and detect total pages."""
    try:
        wait_for_jobs_to_load()
        time.sleep(3)
        total_pages = int(driver.find_element(By.CSS_SELECTOR, "input[type='number']").get_attribute("max") or 1)
        print(f"📄 Total pages detected: {total_pages}")
        return total_pages
    except Exception:
        print("⚠️ Could not determine total pages, defaulting to 1.")
        return 1


def go_to_page(page_number):
    """Change page via input box."""
    try:
        page_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
        driver.execute_script("arguments[0].value = '';", page_input)
        page_input.send_keys(str(page_number))
        page_input.send_keys("\n")
        print(f"➡️ Switching to page {page_number}...")
        wait_for_jobs_to_load()
    except Exception as e:
        print(f"⚠️ Could not switch to page {page_number}: {e}")


# === MAIN FLOW ===
close_popup_initially()  # Only once at start
total_pages = get_total_pages()

for page in range(1, total_pages + 1):
    print(f"\n=============================\n📄 Processing page {page}/{total_pages}\n=============================")
    process_jobs_on_page()
    if page < total_pages:
        go_to_page(page + 1)

print("\n✅ Finished all pages successfully.")
driver.quit()
