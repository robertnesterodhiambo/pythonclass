import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

# Open Rightmove page
driver.get("https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=USERDEFINEDAREA%5E%7B%22polylines%22%3A%22qygwIrto%7E%40qnaE%7BflAwsjCgl%7DAwd%7E%40g%7EvA%7BmLsa%7B%40s%7Cw%40stgKyja%40uusRpkM%7DkrKze_%40mmbFvaf%40%7BdfCdv%7DAcbqDt%7BfA%7DtrAlsyBquaBvedD%7DflAxgeEsia%40pnjW%3FrdiCr%7BZ%7EzdA%7C%60l%40%7Ezm%40znyCnhGthgIdz%7E%40%7E%7B%7EIhh%5Cv%7BlPssd%40xjfDmswA%60wqS%7DacBv%60zFsh%7EBnkuDatdArwg%40s%7EsAr_N%7B%7EbE%7Dre%40mdzG%7DzrBsndD%7Dd_%40o%60%7BC%7D%7Cx%40yzhAucAypi%40%7Ere%40nft%40%7ClE%22%7D")

# Wait for pagination dropdown to appear
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "select[data-testid='paginationSelect']"))
)

# CSV setup (append mode, add headers if file does not exist)
csv_file = "rightmove_data.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Address", "Agent Name", "Phone Number"])  # <-- new column added

def save_to_csv(address, agent, phone):
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([address, agent, phone])

def scrape_current_page():
    # Scroll slowly to bottom to load all listings
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    step = 500
    current = 0
    while current < scroll_height:
        driver.execute_script(f"window.scrollBy(0, {step});")
        current += step
        time.sleep(0.3)
        scroll_height = driver.execute_script("return document.body.scrollHeight")

    # Extract property addresses
    addresses = driver.find_elements(By.CSS_SELECTOR, "address.PropertyAddress_address__LYRPq")
    # Extract agent names
    marketed_elements = driver.find_elements(By.CLASS_NAME, "MarketedBy_joinedText__HTONp")
    # Extract phone numbers
    phone_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='contact-agent-phone-number'] span:first-child")

    # Loop through listings
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
            
        print(address_text, "|", agent_text, "|", phone_text)
        save_to_csv(address_text, agent_text, phone_text)

# Get total pages from dropdown
dropdown = driver.find_element(By.CSS_SELECTOR, "select[data-testid='paginationSelect']")
options = dropdown.find_elements(By.TAG_NAME, "option")
total_pages = len(options)
print(f"Total pages detected: {total_pages}")

current_page = 1
while current_page <= total_pages:
    print(f"\n📄 Scraping page {current_page} of {total_pages} ...")
    scrape_current_page()

    # Go to next page if not last
    if current_page < total_pages:
        next_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='nextPage']")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(3)  # wait for page to load
    current_page += 1

driver.quit()
print("✅ Scraping completed!")
