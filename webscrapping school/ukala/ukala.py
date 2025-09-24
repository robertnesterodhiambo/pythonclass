from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

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

        # Let page load
        time.sleep(5)

        # Click the search link (id="ag_search_name")
        link = driver.find_element(By.ID, "ag_search_name")
        ActionChains(driver).move_to_element(link).click().perform()
        time.sleep(3)

        page = 1
        while True:
            print(f"Currently on page {page}")

            # Scroll to TOP
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)

            # Scroll to BOTTOM
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            try:
                # Look for the "Next >" button
                next_button = driver.find_element(By.XPATH, "//a[@class='js-prevent' and contains(text(),'Next')]")
                # Move and click it
                ActionChains(driver).move_to_element(next_button).click().perform()
                page += 1
                time.sleep(3)
            except:
                print("No more Next button found. Pagination ended.")
                break

    finally:
        driver.quit()

if __name__ == "__main__":
    open_click_and_paginate()
