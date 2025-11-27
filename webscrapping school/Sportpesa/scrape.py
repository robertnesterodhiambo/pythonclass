import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scrape_jackpot_with_carousel(csv_file="jackpot_results.csv"):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # optional
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    collected_data = []  # store (date, picks) tuples

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

        while True:
            # 4️⃣ Collect dates
            date_spans = driver.find_elements(
                By.CSS_SELECTOR, "span.simple-horizontal-carousel__item-title"
            )
            dates = [span.text.strip() for span in date_spans if span.text.strip() != ""]

            # 5️⃣ Expand all jackpot-event-row__winning-pick divs
            parent_divs = driver.find_elements(By.CSS_SELECTOR, "div.jackpot-event-row")
            for parent in parent_divs:
                try:
                    toggle = parent.find_element(By.CSS_SELECTOR, ".jackpot-event-row__toggle")
                    driver.execute_script("arguments[0].click();", toggle)
                    time.sleep(0.1)
                except:
                    pass

            # 6️⃣ Collect picks
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
                    continue  # ignore unknown/empty

            picks_string = "".join(picks_list)

            # 7️⃣ Store date + picks
            for date in dates:
                collected_data.append((date, picks_string))

            # 8️⃣ Save immediately to CSV
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Picks"])
                for row in collected_data:
                    writer.writerow(row)

            print(f"Collected {len(dates)} dates, saved {len(collected_data)} rows to CSV.")

            # 9️⃣ Wait 3 seconds before clicking show more
            time.sleep(3)

            # 10️⃣ Try to click "Show More" button
            try:
                show_more = driver.find_element(
                    By.CSS_SELECTOR,
                    "a.simple-horizontal-carousel__btn.simple-horizontal-carousel__btn--show"
                )
                driver.execute_script("arguments[0].click();", show_more)
                print("Clicked 'Show More' button, loading more dates...")
                time.sleep(3)  # wait for new content to load
            except:
                print("'Show More' button not found. Finished collecting all data.")
                break  # exit loop if button is gone

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_jackpot_with_carousel()
