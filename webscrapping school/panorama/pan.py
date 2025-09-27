import time
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Setup ---
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Load Excel ---
df = pd.read_excel("Project.xlsx")
cities = df["City"].dropna().tolist()

# --- CSV Setup ---
output_file = "results.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["City", "Company", "CompanyLink"])

# --- Open Website ---
driver.get("https://panoramafirm.pl/")

# --- Enter 'obróbka metali' in first input ---
what_input = driver.find_element(By.ID, "search-what")
what_input.clear()
for ch in "obróbka metali":
    what_input.send_keys(ch)
    time.sleep(0.1)

# --- Loop through cities ---
for city in cities:
    where_input = driver.find_element(By.ID, "search-where")
    where_input.clear()

    # Type city letter by letter
    for ch in city:
        where_input.send_keys(ch)
        time.sleep(0.1)

    where_input.send_keys(Keys.ENTER)

    # Wait for company list
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "company-list"))
        )
    except:
        print(f"No results for {city}")
        continue

    # Scroll to bottom (to load all results)
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # ✅ Collect company names + links
    companies = driver.find_elements(By.CSS_SELECTOR, "h2.font-weight-bold.mb-0 a.company-name")

    results = [(city, c.text.strip(), c.get_attribute("href")) for c in companies if c.text.strip()]

    # Append to CSV
    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print(f"✅ {len(results)} companies collected for {city}")

driver.quit()
print("🎉 Done! All results saved to results.csv")
