import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Automatically download and install correct chromedriver
chromedriver_autoinstaller.install()

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Initialize Chrome with autoinstalled driver
driver = webdriver.Chrome(options=options)

# Open the target page
driver.get("https://inpi.justica.gov.pt/boletim-da-propriedade-industrial")

time.sleep(5)
print("Page title:", driver.title)

driver.quit()
