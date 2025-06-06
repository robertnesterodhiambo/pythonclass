from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup Chrome
options = Options()
# options.add_argument("--headless")  # Optional: run in headless mode
driver = webdriver.Chrome(options=options)
driver.get("https://www.shipito.com/en/shipping-calculator")

wait = WebDriverWait(driver, 20)

# ✅ STEP 1: Click the toggle button inside the warehouse dropdown
toggle_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.warehouse-list button.btn.dropdown-toggle"))
)
toggle_button.click()

# ✅ STEP 2: Wait for the dropdown menu to appear
dropdown_menu = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.warehouse-list.open ul.dropdown-menu"))
)

# ✅ STEP 3: Get all <a> options inside the dropdown list
warehouse_items = dropdown_menu.find_elements(By.CSS_SELECTOR, "li > a.field-selector")

# ✅ STEP 4: Click each one in a loop
for i in range(len(warehouse_items)):
    item = warehouse_items[i]
    name = item.text
    value = item.get_attribute("data-value")
    print(f"Clicking warehouse: {name} (data-value={value})")

    item.click()
    time.sleep(2)

    # Reopen the dropdown toggle for the next selection
    toggle_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.warehouse-list button.btn.dropdown-toggle"))
    )
    toggle_button.click()

    dropdown_menu = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.warehouse-list.open ul.dropdown-menu"))
    )
    warehouse_items = dropdown_menu.find_elements(By.CSS_SELECTOR, "li > a.field-selector")

# ✅ Done
driver.quit()
