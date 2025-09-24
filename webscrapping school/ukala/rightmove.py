import time
import csv
import os
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

# CSV setup
csv_file = "rightmove_addresses.csv"
file_exists = os.path.isfile(csv_file)

# Open CSV in append mode
with open(csv_file, "a", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["address"])
    
    # Write header only if file didn't exist
    if not file_exists:
        writer.writeheader()

    collected = set()  # To avoid duplicates in this session

    # Scroll down slowly to load all properties
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = 500
    current = 0

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
                writer.writerow({"address": text})  # save immediately
                csvfile.flush()  # ensure it's written to disk
                collected.add(text)
                print(text)  # print to terminal in real time

print("\n✅ All visible addresses saved/appended to rightmove_addresses.csv")
driver.quit()
