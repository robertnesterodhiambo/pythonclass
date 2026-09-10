from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import os


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

CSV_FILE = "jackpot_results.csv"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)


# ---------------------------------------------------------
# CREATE CSV
# ---------------------------------------------------------

csv_exists = os.path.exists(CSV_FILE)

csv_file = open(
    CSV_FILE,
    "a",
    newline="",
    encoding="utf-8"
)

writer = csv.DictWriter(
    csv_file,
    fieldnames=[
        "date",
        "teams",
        "result",
        "outcome",
        "link"
    ]
)

if not csv_exists:
    writer.writeheader()
    csv_file.flush()


try:

    # -----------------------------------------------------
    # OPEN WEBSITE
    # -----------------------------------------------------

    driver.get("https://www.ke.sportpesa.com/en/mega-jackpot-pro/results")

    input(
        "Interact with the website, then press ENTER here..."
    )


    # -----------------------------------------------------
    # FIND IFRAME
    # -----------------------------------------------------

    iframe = wait.until(
        EC.presence_of_element_located(
            (By.ID, "multijackpot-iframe")
        )
    )

    driver.switch_to.frame(iframe)

    print("Switched into iframe.")
    print("-" * 60)


    # -----------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------

    while True:

        print("Looking for event rows...")


        # -------------------------------------------------
        # GET ONLY REAL EVENT ROWS
        # EXCLUDE:
        # jackpot-event-row__header
        # -------------------------------------------------

        rows = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row:not(.jackpot-event-row__header)"
                )
            )
        )

        print(f"Found {len(rows)} real event(s).")


        # -------------------------------------------------
        # FIND NEXT BUTTON
        # -------------------------------------------------

        next_button = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "div.simple-horizontal-carousel__container > a.simple-horizontal-carousel__btn"
                )
            )
        )


        # Get the link for this page
        link = next_button.get_attribute("href")


        # -------------------------------------------------
        # EXTRACT DATA
        # -------------------------------------------------

        for row in rows:

            try:

                date = row.find_element(
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row__date"
                ).text.strip()


                teams = row.find_element(
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row__event-name"
                ).text.strip()


                result = row.find_element(
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row__result"
                ).text.strip()


                outcome = row.find_element(
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row__winning-pick"
                ).text.strip()


                # Remove labels
                result = result.replace(
                    "RESULT :",
                    ""
                ).strip()

                outcome = outcome.replace(
                    "OUTCOME :",
                    ""
                ).strip()


                # -------------------------------------------------
                # SAVE IMMEDIATELY
                # -------------------------------------------------

                writer.writerow({
                    "date": date,
                    "teams": teams,
                    "result": result,
                    "outcome": outcome,
                    "link": link
                })

                csv_file.flush()


                print(
                    f"Saved: {date} | "
                    f"{teams} | "
                    f"{result} | "
                    f"{outcome} | "
                    f"{link}"
                )


            except Exception as e:

                print(
                    f"Could not extract event: {e}"
                )


        print("-" * 60)
        print("Current page saved.")
        print("Clicking NEXT...")


        # -------------------------------------------------
        # SCROLL NEXT BUTTON INTO VIEW
        # -------------------------------------------------

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            next_button
        )


        # -------------------------------------------------
        # CLICK NEXT
        # -------------------------------------------------

        next_button.click()

        print("NEXT clicked.")


        # -------------------------------------------------
        # WAIT FOR NEW EVENTS
        # -------------------------------------------------

        wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row:not(.jackpot-event-row__header)"
                )
            )
        )

        print("New content loaded.")
        print("-" * 60)


except KeyboardInterrupt:

    print("\nScraper stopped by user.")


finally:

    csv_file.close()
    driver.quit()

    print(f"\nCSV saved as: {CSV_FILE}")