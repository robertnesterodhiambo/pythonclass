import os
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
    """Wait until the pagination control appears (current page item visible)."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li.circle-pagination__item.current"))
    )

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

        # Always click the agent search button to trigger pagination
        link = driver.find_element(By.ID, "ag_search_name")
        ActionChains(driver).move_to_element(link).click().perform()
        print("Clicked agent search button, waiting for pagination to appear...")
        wait_for_pagination(driver, timeout=20)
        print("Pagination detected!")

        while True:
            current_page = get_active_page(driver)
            if not current_page:
                print("Could not detect current page, stopping.")
                break

            print(f"Currently on page {current_page}")
            save_progress(current_page)

            # Scroll to top
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1.5)

            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                # Try clicking "Next >"
                next_button = driver.find_element(By.XPATH, "//a[@class='js-prevent' and contains(text(),'Next')]")
                ActionChains(driver).move_to_element(next_button).click().perform()
                wait_for_page_change(driver, current_page)
            except:
                print("No Next button found, checking last page number...")
                try:
                    last_page = driver.find_elements(By.CSS_SELECTOR, "ul.circle-pagination li a")[-1]
                    ActionChains(driver).move_to_element(last_page).click().perform()
                    wait_for_page_change(driver, current_page)
                except:
                    print("Reached the last page. Pagination ended.")
                    break

    finally:
        driver.quit()

if __name__ == "__main__":
    open_click_and_paginate()
