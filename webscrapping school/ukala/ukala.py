from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def open_and_simulate_click():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.ukala.org.uk/agent-search/ukala-agent-directory/"
        driver.get(url)

        # Wait for the page to load
        time.sleep(5)

        # Find the link
        link = driver.find_element(By.ID, "ag_search_name")

        # --- Option 1: ActionChains (mouse click simulation) ---
        actions = ActionChains(driver)
        actions.move_to_element(link).click().perform()

        # --- Option 2: Simulate pressing ENTER key ---
        # link.send_keys(Keys.ENTER)

        time.sleep(30)
        print("Simulated a real user click on ag_search_name!")

    finally:
        driver.quit()

if __name__ == "__main__":
    open_and_simulate_click()
