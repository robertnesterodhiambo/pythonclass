from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def open_and_scroll_iframe_root():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # optional

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    try:
        url = "https://www.ke.sportpesa.com/en/mega-jackpot-pro/results"
        driver.get(url)

        # 1️⃣ Wait for iframe to appear
        print("Waiting for iframe...")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "multijackpot-iframe"))
        )
        print("Iframe loaded")

        # 2️⃣ Switch to the iframe
        driver.switch_to.frame(iframe)
        print("Switched to iframe")

        # 3️⃣ Wait for #root div inside iframe
        root_div = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        print("#root div found inside iframe")

        # 4️⃣ Scroll #root to bottom
        last_height = driver.execute_script(
            "return document.getElementById('root').scrollHeight;"
        )

        while True:
            driver.execute_script("""
                document.getElementById('root')
                .scrollTo(0, document.getElementById('root').scrollHeight);
            """)
            time.sleep(1)

            new_height = driver.execute_script(
                "return document.getElementById('root').scrollHeight;"
            )

            if new_height == last_height:
                print("Reached bottom of #root")
                break

            last_height = new_height

        print("Scrolling complete")
        time.sleep(2)

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()


if __name__ == "__main__":
    open_and_scroll_iframe_root()
