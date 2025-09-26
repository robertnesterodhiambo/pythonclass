import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Price ranges ---
prices = [
    50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 125000, 130000,
    140000, 150000, 160000, 170000, 175000, 180000, 190000, 200000, 210000,
    220000, 230000, 240000, 250000, 260000, 270000, 280000, 290000, 300000,
    325000, 350000, 375000, 400000, 425000, 450000, 475000, 500000
]

# --- Bedroom ranges ---
bedrooms = list(range(0, 11))  # 0 = Studio, 1–10 beds

# --- Base URL ---
base_url = (
    "https://www.rightmove.co.uk/property-for-sale/find.html?"
    "locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22aztmHt%60bg%40xoKibcUqcc%40mquEiopAudtI%7De_FsxzJyn%60%40irVmgqBs%7BZ_dhG%3FgsbMsen%40%7D%7CfJ%3F_t%7BA%7Cd_%40acjBfbjAw%60p%40dx%7DCoc_%40bj%7EFvcUhecJ%3Fj%7EhRp_%5DhsiJ%7EhlAh_cI%60%7BzAd%7E%7DD%60uqAdvpBjhzCznyCflbKdhjBnnjBjvI%7CrcI%7ChRblqDsen%40foeC%7BzrBhkf%40qknA%60giEgrvVh%7CLgr%7DByoKrg%7BA%22%7D"
    "&sortType=6&channel=BUY&transactionType=BUY&displayLocationIdentifier=undefined"
)

# --- Setup ChromeDriver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# --- CSV setup ---
csv_file = "rightmove_data.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Agent Name", "Phone Number", "MinPrice", "MaxPrice", "Bedrooms"])

def save_to_csv(address, agent, phone, min_price, max_price, beds):
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([address, agent, phone, min_price, max_price, beds])

def scrape_current_page(min_price, max_price, beds):
    # Scroll slowly to bottom to load all listings
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = 500
    current = 0
    while current < scroll_height:
        driver.execute_script(f"window.scrollBy(0, {step});")
        current += step
        time.sleep(0.3)
        scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Extract data
    addresses = driver.find_elements(By.CSS_SELECTOR, "address.PropertyAddress_address__LYRPq")
    marketed_elements = driver.find_elements(By.CLASS_NAME, "MarketedBy_joinedText__HTONp")
    phone_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='contact-agent-phone-number'] span:first-child")

    for i in range(len(addresses)):
        address_text = addresses[i].text.strip()
        agent_text = ""
        phone_text = ""

        if i < len(marketed_elements):
            full_text = marketed_elements[i].text.strip()
            if " by " in full_text:
                agent_text = full_text.split(" by ", 1)[1].strip()

        if i < len(phone_elements):
            phone_text = phone_elements[i].text.strip()

        print(address_text, "|", agent_text, "|", phone_text, "|", min_price, "-", max_price, "|", beds, "beds")
        save_to_csv(address_text, agent_text, phone_text, min_price, max_price, beds)

# --- Loop through beds and price ranges ---
for beds in bedrooms:
    for i in range(len(prices)-1):
        min_price = prices[i]
        max_price = prices[i+1]
        url = f"{base_url}&minPrice={min_price}&maxPrice={max_price}&minBedrooms={beds}&maxBedrooms={beds}&index=0"

        print(f"\n💰 Scraping £{min_price} - £{max_price} | 🛏 {beds} beds")

        driver.get(url)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='paginationSelect']"))
            )
        except:
            print("⚠ No results for this range.")
            continue

        # Total pages in this range
        dropdown = driver.find_element(By.CSS_SELECTOR, "select[data-testid='paginationSelect']")
        options = dropdown.find_elements(By.TAG_NAME, "option")
        total_pages = len(options)
        current_page = 1

        while current_page <= total_pages:
            print(f"📄 Scraping page {current_page} of {total_pages}")
            scrape_current_page(min_price, max_price, beds)

            if current_page < total_pages:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='nextPage']")
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                except:
                    break
            current_page += 1

driver.quit()
print("✅ Scraping completed!")
