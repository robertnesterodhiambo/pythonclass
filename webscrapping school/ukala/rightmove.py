import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Automatically download & set up the right ChromeDriver
service = Service(ChromeDriverManager().install())

# Launch Chrome
driver = webdriver.Chrome(service=service)

# Open Rightmove
driver.get("https://www.rightmove.co.uk/property-for-sale/find.html?sortType=10&areaSizeUnit=sqft&channel=BUY&index=0&locationIdentifier=REGION%5E92048&transactionType=BUY&displayLocationIdentifier=East-Anglia.html")

# Maximize the window
driver.maximize_window()

# Wait only for pagination button to appear, no full page wait
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Pagination_button__5gDab"))
)

print("✅ Pagination button appeared, start scrolling...")

# Now scroll down slowly in steps
scroll_height = driver.execute_script("return document.body.scrollHeight")
step = 500  # pixels per scroll
current = 0

while current < scroll_height:
    driver.execute_script(f"window.scrollBy(0, {step});")
    current += step
    time.sleep(0.5)  # slow scrolling
    scroll_height = driver.execute_script("return document.body.scrollHeight")

# Stay at bottom for a moment
time.sleep(3)

# Close browser
driver.quit()
