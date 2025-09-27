import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://panoramafirm.pl/"
text_to_type = "obróbka metali"

# Chrome setup
opts = Options()
# opts.add_argument("--headless=new")   # uncomment for headless mode
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)

try:
    driver.get(url)

    # Wait for the input field to be present
    wait = WebDriverWait(driver, 15)
    search_input = wait.until(EC.presence_of_element_located((By.ID, "search-what")))

    # Clear any pre-filled text
    search_input.clear()

    # Type letter by letter
    for char in text_to_type:
        search_input.send_keys(char)
        time.sleep(0.2)  # delay between keystrokes (adjust if needed)

    print("✅ Finished typing into search box.")

    # Optional: take screenshot to confirm
    driver.save_screenshot("typed_search.png")

finally:
    driver.quit()
