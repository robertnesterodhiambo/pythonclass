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
# CREATE CSV IF IT DOES NOT EXIST
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

    # Manually interact with the page
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

    # Switch into iframe
    driver.switch_to.frame(iframe)

    print("Switched into iframe.")
    print("-" * 60)


    # -----------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------

    while True:

        print("Looking for event rows...")

        # Find all event rows currently displayed
        rows = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row"
                )
            )
        )

        print(f"Found {len(rows)} event(s).")


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

        # Save the link before clicking
        link = next_button.get_attribute("href")


        # -------------------------------------------------
        # EXTRACT EACH EVENT
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

                # Remove "RESULT :" if present
                result = result.replace(
                    "RESULT :",
                    ""
                ).strip()


                outcome = row.find_element(
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row__winning-pick"
                ).text.strip()

                # Remove "OUTCOME :" if present
                outcome = outcome.replace(
                    "OUTCOME :",
                    ""
                ).strip()


                # -------------------------------------------------
                # SAVE IMMEDIATELY TO CSV
                # -------------------------------------------------

                writer.writerow({
                    "date": date,
                    "teams": teams,
                    "result": result,
                    "outcome": outcome,
                    "link": link
                })

                # Force data to disk immediately
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
                    f"Could not extract one event: {e}"
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
        # WAIT FOR NEW CONTENT
        # -------------------------------------------------

        # Wait until the page has event rows again
        wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row"
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
