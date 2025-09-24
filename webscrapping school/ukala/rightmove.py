import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Create a dedicated profile folder for Selenium
selenium_profile = os.path.expanduser("~/.config/selenium_chrome")

options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir={selenium_profile}")
options.add_argument("--profile-directory=Default")
options.add_argument("--start-maximized")

# Extra flags to avoid common crashes
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")

# Keep browser open after script finishes
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.rightmove.co.uk")

time.sleep(10)
