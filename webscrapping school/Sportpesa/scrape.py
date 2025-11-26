import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_dates_and_save_csv(csv_file="dates.csv"):
    # Setup Chrome
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

        # 1️⃣ Wait for iframe
        print("Waiting for iframe...")
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "multijackpot-iframe"))
        )
        print("Iframe loaded")

        # 2️⃣ Switch to iframe
        driver.switch_to.frame(iframe)
        print("Switched to iframe")

        # 3️⃣ Wait for #root inside iframe
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

        # 5️⃣ Collect all dates
        date_spans = driver.find_elements(
            By.CSS_SELECTOR, "span.simple-horizontal-carousel__item-title"
        )
        dates = [span.text.strip() for span in date_spans if span.text.strip() != ""]
        print(f"Collected {len(dates)} dates")

        # 6️⃣ Save immediately to CSV
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date"])
            for date in dates:
                writer.writerow([date])

        print(f"Saved dates to {csv_file}")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_dates_and_save_csv()
