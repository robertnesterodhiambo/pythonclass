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
        writer.writerow([
            "jobtitle",
            "link",
            "gross_salary",
            "job_openings",
            "phone_number",
            "email",
            "contact_person",
            "employer",
            "work_location"
        ])


def save_job_data(title, link, salary, openings, phone, email, contact, employer, work_location):
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([title, link, salary, openings, phone, email, contact, employer, work_location])
    print(f"💾 Saved: {title} | {link} | {salary} | {openings} | {phone} | {email} | {contact} | {employer} | {work_location}")


def close_popup_initially():
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
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.icon-link")))
        time.sleep(1)
        print("✅ Job list loaded.")
    except TimeoutException:
        print("⚠️ Job list did not fully load.")


def process_jobs_on_page(current_page):
    try:
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
                time.sleep(5)

                try:
                    label = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "label.xng-breadcrumb-trail"))
                    )
                    label_text = label.text.strip()
                    job_link = driver.current_url  # ✅ Capture current job link

                    # === Gross Salary / Stypendium brutto ===
                    try:
                        gross_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[contains(., 'Wynagrodzenie brutto') or contains(., 'Stypendium brutto')]]//span[@class='details-row-value']"
                        )
                        gross_salary = gross_elem.text.strip()
                    except Exception:
                        gross_salary = "(not listed)"

                    # === Number of Job Openings ===
                    try:
                        openings_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[contains(., 'Liczba miejsc pracy:')]]//span[@class='details-row-value']"
                        )
                        job_openings = openings_elem.text.strip()
                    except Exception:
                        job_openings = "(not listed)"

                    # === Phone Number ===
                    try:
                        phone_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[contains(., 'Numer telefonu:')]]//a"
                        )
                        phone_number = phone_elem.text.strip()
                    except Exception:
                        phone_number = "(not found)"

                    # === Email ===
                    try:
                        email_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[normalize-space()='E-mail:']]//span[@class='details-row-value']"
                        )
                        email = email_elem.text.strip() if email_elem.text.strip() else "(not found)"
                    except Exception:
                        email = "(not found)"

                    # === Contact Person ===
                    try:
                        contact_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[contains(., 'Osoba do kontaktu Pracodawcy:')]]//span[@class='details-row-value']"
                        )
                        contact_person = contact_elem.text.strip()
                    except Exception:
                        contact_person = "(not found)"

                    # === Employer ===
                    try:
                        employer_elem = driver.find_element(
                            By.XPATH,
                            "//ng-component[.//span[contains(., 'Pracodawca:')]]//span[@class='details-row-value']"
                        )
                        employer = employer_elem.text.strip()
                    except Exception:
                        employer = "(not found)"

                    # === Work Location (Adres:) ===
                    try:
                        location_elem = driver.find_element(
                            By.XPATH,
                            "//cbop-row-map[.//span[contains(., 'Adres:')]]//div"
                        )
                        work_location = location_elem.text.strip()
                    except Exception:
                        work_location = "(not found)"

                    save_job_data(
                        label_text,
                        job_link,
                        gross_salary,
                        job_openings,
                        phone_number,
                        email,
                        contact_person,
                        employer,
                        work_location
                    )

                except Exception:
                    print("⚠️ Could not find job title label after 5 seconds.")
                    save_job_data(
                        "(missing title)",
                        driver.current_url,
                        "(not listed)",
                        "(not listed)",
                        "(not found)",
                        "(not found)",
                        "(not found)",
                        "(not found)",
                        "(not found)"
                    )

                driver.back()
                wait_for_jobs_to_load()

            except (TimeoutException, StaleElementReferenceException):
                print("⚠️ Skipped due to timeout or stale element.")
                driver.back()
                wait_for_jobs_to_load()
                continue

    except IndexError:
        print("❌ IndexError: Job list became unstable.")
        print("⏸️ Pausing for 5 minutes before retrying...")
        time.sleep(300)
        print("🔄 Reloading site and resuming from last page...")
        driver.get(url)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        close_popup_initially()
        go_to_page(current_page)
        process_jobs_on_page(current_page)


def get_total_pages():
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
    try:
        page_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='number']")))
        driver.execute_script("arguments[0].value = '';", page_input)
        page_input.send_keys(str(page_number))
        page_input.send_keys("\n")
        print(f"➡️ Switching to page {page_number}...")
        wait_for_jobs_to_load()
    except Exception as e:
        print(f"⚠️ Could not switch to page {page_number}: {e}")


# === CHECKPOINT SYSTEM ===
CHECKPOINT_FILE = "checkpoint.txt"

def save_checkpoint(page):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(page))
    print(f"💾 Checkpoint saved: page {page}")

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 1
    return 1


# === MAIN FLOW ===
close_popup_initially()
total_pages = get_total_pages()

start_page = load_checkpoint()
if start_page > 1:
    print(f"⏩ Resuming from saved checkpoint: page {start_page}")
    go_to_page(start_page)

for page in range(start_page, total_pages + 1):
    print(f"\n=============================\n📄 Processing page {page}/{total_pages}\n=============================")
    process_jobs_on_page(page)
    save_checkpoint(page)
    if page < total_pages:
        go_to_page(page + 1)

if os.path.exists(CHECKPOINT_FILE):
    os.remove(CHECKPOINT_FILE)
    print("🧹 Checkpoint cleared after completion.")

print("\n✅ Finished all pages successfully.")
driver.quit()
