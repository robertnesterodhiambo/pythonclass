from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def open_click_and_scroll():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = "https://www.ukala.org.uk/agent-search/ukala-agent-directory/"
        driver.get(url)

        # Let page load
        time.sleep(5)

        # Find the link
        link = driver.find_element(By.ID, "ag_search_name")

        # Simulate a real user click with ActionChains
        actions = ActionChains(driver)
        actions.move_to_element(link).click().perform()

        # Wait after click
        time.sleep(3)

        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait after scrolling
        time.sleep(5)

        print("Clicked, scrolled to bottom, and waited!")

    finally:
        driver.quit()

if __name__ == "__main__":
    open_click_and_scroll()
