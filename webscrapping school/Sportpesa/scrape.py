import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_dates_and_picks(csv_file="jackpot_results.csv"):
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
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "multijackpot-iframe"))
        )
        driver.switch_to.frame(iframe)

        # 2️⃣ Wait for #root inside iframe
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "root"))
        )

        # 3️⃣ Scroll #root to bottom to load all content
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
                break
            last_height = new_height

        # 4️⃣ Collect all dates
        date_spans = driver.find_elements(
            By.CSS_SELECTOR, "span.simple-horizontal-carousel__item-title"
        )
        dates = [span.text.strip() for span in date_spans if span.text.strip() != ""]
        print(f"Collected {len(dates)} dates")

        # 5️⃣ Expand hidden jackpot-event-row__winning-pick divs (if needed)
        parent_divs = driver.find_elements(By.CSS_SELECTOR, "div.jackpot-event-row")
        for parent in parent_divs:
            try:
                toggle = parent.find_element(By.CSS_SELECTOR, ".jackpot-event-row__toggle")
                driver.execute_script("arguments[0].click();", toggle)
                time.sleep(0.2)
            except:
                pass

        # 6️⃣ Collect winning picks
        picks_divs = driver.find_elements(By.CSS_SELECTOR, "div.jackpot-event-row__winning-pick")
        picks_list = []
        for div in picks_divs:
            text = div.text.strip().lower()
            if "home" in text:
                picks_list.append("1")
            elif "away" in text:
                picks_list.append("2")
            elif "draw" in text:
                picks_list.append("X")
            else:
                picks_list.append("?")

        picks_string = "".join(picks_list)
        print("Collected picks string:", picks_string)

        # 7️⃣ Save Date + Picks to CSV
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Picks"])
            for date in dates:
                writer.writerow([date, picks_string])  # same picks for all dates on page

        print(f"Saved Date + Picks to {csv_file}")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_dates_and_picks()
