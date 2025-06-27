import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Install matching chromedriver
chromedriver_autoinstaller.install()

# Chrome setup
options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://inpi.justica.gov.pt/boletim-da-propriedade-industrial")

# Wait for the first .wrapper to load
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
)

# Get first .wrapper div
first_wrapper = driver.find_element(By.CLASS_NAME, "wrapper")

# Find the <a> inside it
link = first_wrapper.find_element(By.TAG_NAME, "a")

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
time.sleep(1)

# Click the link (opens in new tab)
link.click()

# Wait for the new tab and switch to it
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])

# Wait for new tab content to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

print("New tab title:", driver.title)
time.sleep(5)
driver.quit()
