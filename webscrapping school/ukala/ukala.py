import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

PROGRESS_FILE = "progress.txt"
CSV_FILE = "ukala_agents.csv"

def save_progress(page_number):
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(page_number))

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 1
    return 1

def get_active_page(driver):
    try:
        active = driver.find_element(By.CSS_SELECTOR, "li.circle-pagination__item.current a")
        return int(active.get_attribute("data-page"))
    except:
        return None

def wait_for_page_change(driver, old_page, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: get_active_page(d) != old_page
    )

def wait_for_pagination(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.circle-pagination__item.current"))
    )

def go_to_saved_page(driver, saved_page):
    while True:
        current_page = get_active_page(driver)
        if not current_page:
            break
        if current_page >= saved_page:
            print(f"Resumed at saved page {current_page}")
            break
        try:
            next_button = driver.find_element(By.XPATH, "//a[@class='js-prevent' and contains(text(),'Next')]")
            ActionChains(driver).move_to_element(next_button).click().perform()
            wait_for_page_change(driver, current_page)
        except:
            break

def collect_and_save(driver, current_page):
    items = driver.find_elements(By.CSS_SELECTOR, "div.partner-item.partner-item--small-padding")
    found_any = False

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for item in items:
            try:
                name = item.find_element(By.CSS_SELECTOR, ".partner-item__name").text.strip()
            except:
                name = ""

            try:
                excerpt = item.find_element(By.CSS_SELECTOR, ".partner-item__excerpt").text.strip()
            except:
                excerpt = ""

            # Print everything for confirmation
            print(f"[Page {current_page}] Found: {name} - {excerpt}")

            # Save only numbers starting with 07
            if excerpt.startswith("07"):
                writer.writerow([name, excerpt])
                print(f"✅ Saved to CSV: {name} - {excerpt}")
                found_any = True

    if not found_any:
        print(f"[Page {current_page}] No numbers starting with 07 were found.")

def open_click_and_paginate():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.ukala.org.uk/agent-search/ukala-agent-directory/"
        driver.get(url)
        time.sleep(5)

        # Always click the agent search button
        link = driver.find_element(By.ID, "ag_search_name")
        ActionChains(driver).move_to_element(link).click().perform()
        print("Clicked agent search button, waiting for pagination...")
        wait_for_pagination(driver, timeout=20)

        saved_page = load_progress()
        if saved_page > 1:
            go_to_saved_page(driver, saved_page)

        while True:
            current_page = get_active_page(driver)
            if not current_page:
                print("Could not detect current page, stopping.")
                break

            print(f"📄 Currently on page {current_page}")
            save_progress(current_page)

            # Collect and save data for this page
            collect_and_save(driver, current_page)

            # Scroll top → bottom
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                next_button = driver.find_element(By.XPATH, "//a[@class='js-prevent' and contains(text(),'Next')]")
                ActionChains(driver).move_to_element(next_button).click().perform()
                wait_for_page_change(driver, current_page)
            except:
                print("No Next button found, checking last page...")
                try:
                    last_page = driver.find_elements(By.CSS_SELECTOR, "ul.circle-pagination li a")[-1]
                    ActionChains(driver).move_to_element(last_page).click().perform()
                    wait_for_page_change(driver, current_page)
                except:
                    print("Reached last page. Pagination ended.")
                    break

    finally:
        driver.quit()

if __name__ == "__main__":
    # Ensure CSV file has header if starting fresh
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone"])
    open_click_and_paginate()
