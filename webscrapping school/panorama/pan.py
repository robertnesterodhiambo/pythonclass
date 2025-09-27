import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# URL and Excel file
url = "https://panoramafirm.pl/"
excel_file = "Project.xlsx"
column_name = "City:"

# Load Excel file
df = pd.read_excel(excel_file)
cities = df[column_name].dropna().tolist()

# Chrome setup
opts = Options()
# opts.add_argument("--headless=new")   # uncomment for headless mode
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)

try:
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # Type "obróbka metali" into search-what (once)
    search_what = wait.until(EC.presence_of_element_located((By.ID, "search-what")))
    search_what.clear()
    for ch in "obróbka metali":
        search_what.send_keys(ch)
        time.sleep(0.2)

    # Loop through cities
    for city in cities:
        print(f"🔎 Searching for city: {city}")

        # Re-locate search-where fresh every time (avoids stale reference)
        search_where = wait.until(EC.presence_of_element_located((By.ID, "search-where")))
        search_where.clear()

        # Type letter by letter
        for ch in str(city):
            search_where.send_keys(ch)
            time.sleep(0.2)

        # Press Enter to search
        search_where.send_keys(Keys.ENTER)

        # Wait for page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        print(f"✅ Loaded results for {city}")

        # Small pause before next city
        time.sleep(2)

finally:
    driver.quit()
