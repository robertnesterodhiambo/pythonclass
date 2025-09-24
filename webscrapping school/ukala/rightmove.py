import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open Rightmove
driver.get("https://www.rightmove.co.uk/property-for-sale/find.html?sortType=10&areaSizeUnit=sqft&channel=BUY&index=0&locationIdentifier=REGION%5E92048&transactionType=BUY&displayLocationIdentifier=East-Anglia.html")
driver.maximize_window()

# Wait for pagination button to appear
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Pagination_button__5gDab"))
)
print("✅ Pagination button appeared, start scrolling...")

# Open CSV file for writing addresses
with open("rightmove_addresses.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["address"])
    writer.writeheader()

    # Scroll down slowly to load all properties
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = 500
    current = 0
    collected = set()  # to avoid duplicates

    while current < scroll_height:
        driver.execute_script(f"window.scrollBy(0, {step});")
        current += step
        time.sleep(0.5)
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        # Extract all addresses visible so far
        addresses = driver.find_elements(By.CLASS_NAME, "PropertyAddress_address__LYRPq")
        for addr in addresses:
            text = addr.text.strip()
            if text and text not in collected:
                writer.writerow({"address": text})
                collected.add(text)
                print(text)  # print to terminal in real time

    # One last extraction after finishing scroll
    addresses = driver.find_elements(By.CLASS_NAME, "PropertyAddress_address__LYRPq")
    for addr in addresses:
        text = addr.text.strip()
        if text and text not in collected:
            writer.writerow({"address": text})
            collected.add(text)
            print(text)

print("\n✅ All addresses saved to rightmove_addresses.csv")
driver.quit()
