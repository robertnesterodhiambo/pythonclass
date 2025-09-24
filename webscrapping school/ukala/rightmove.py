import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Set up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open Rightmove
driver.get("https://www.rightmove.co.uk/property-for-sale/find.html?sortType=10&areaSizeUnit=sqft&channel=BUY&index=0&locationIdentifier=REGION%5E92048&transactionType=BUY&displayLocationIdentifier=East-Anglia.html")
driver.maximize_window()

# CSV setup
csv_file = "rightmove_addresses.csv"
file_exists = os.path.isfile(csv_file)

with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["address"])
    if not file_exists:
        writer.writeheader()

    collected = set()  # To avoid duplicates in this session

    while True:
        # Wait for properties to load
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "PropertyAddress_address__LYRPq"))
            )
        except TimeoutException:
            print("⚠️ Timeout waiting for properties.")
            break

        # Collect addresses on current page
        addresses = driver.find_elements(By.CLASS_NAME, "PropertyAddress_address__LYRPq")
        for addr in addresses:
            text = addr.text.strip()
            if text and text not in collected:
                writer.writerow({"address": text})
                csvfile.flush()  # Save immediately
                collected.add(text)
                print(text)

        # Identify last page from dropdown
        try:
            dropdown = driver.find_element(By.CSS_SELECTOR, "select[data-testid='paginationSelect']")
            options = dropdown.find_elements(By.TAG_NAME, "option")
            last_page_index = int(options[-1].get_attribute("value"))  # last page value
            current_page_index = int(dropdown.find_element(By.CSS_SELECTOR, "option[selected]").get_attribute("value"))

            if current_page_index >= last_page_index:
                print("✅ Reached last page.")
                break  # stop scraping

            # Click next page
            next_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='nextPage']")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            next_button.click()
            print("➡️ Moved to next page...")
            time.sleep(3)  # wait for next page to load

        except (NoSuchElementException, TimeoutException):
            print("❌ Cannot find pagination dropdown or next button, stopping.")
            break

print("\n✅ Scraping completed. Addresses saved/appended to rightmove_addresses.csv")
driver.quit()
