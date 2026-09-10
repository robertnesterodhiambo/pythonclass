from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--start-maximized")

# Selenium automatically:
# 1. Detects Chrome
# 2. Finds the appropriate ChromeDriver
# 3. Downloads it if necessary
# 4. Starts Chrome
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.ke.sportpesa.com/en/mega-jackpot-pro/results")

    print("Browser opened successfully")
    print("Title:", driver.title)
    print("URL:", driver.current_url)

    input("Press Enter to close...")

finally:
    driver.quit()