from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
# CREATE / LOAD CSV
# ---------------------------------------------------------

csv_exists = os.path.exists(CSV_FILE)

# Store all existing links from the CSV
existing_links = set()

if csv_exists:

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as existing_file:

        reader = csv.DictReader(existing_file)

        for existing_row in reader:

            existing_link = existing_row.get("link")

            if existing_link:
                existing_links.add(existing_link)

    print(
        f"Existing CSV found."
        f" {len(existing_links)} existing link(s) loaded."
    )

else:

    print("CSV does not exist. A new CSV will be created.")


# ---------------------------------------------------------
# OPEN CSV FOR APPENDING
# ---------------------------------------------------------

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

    driver.get(
        "https://www.ke.sportpesa.com/en/mega-jackpot-pro/results"
    )

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

    # Switch Selenium into the iframe
    driver.switch_to.frame(iframe)

    print("Switched into iframe.")
    print("-" * 60)


    # -----------------------------------------------------
    # MAIN LOOP
    # -----------------------------------------------------

    while True:

        print("Looking for event rows...")


        # -------------------------------------------------
        # FIND ONLY REAL EVENT ROWS
        # EXCLUDE THE HEADER
        # -------------------------------------------------

        rows = wait.until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    "div.jackpot-event-row:not(.jackpot-event-row__header)"
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


        # -------------------------------------------------
        # GET LINK
        # -------------------------------------------------

        link = next_button.get_attribute("href")

        print(f"Link: {link}")


        # -------------------------------------------------
        # CHECK IF THIS PAGE ALREADY EXISTS
        # -------------------------------------------------

        if link in existing_links:

            print(
                f"SKIPPED:"
                f" Link already exists in CSV."
            )

            print(
                f"Already existing link: {link}"
            )

            print("-" * 60)
            print("No new data saved from this page.")


        else:

            print(
                "New link found."
                " Saving events..."
            )


            # -------------------------------------------------
            # EXTRACT EACH EVENT
            # -------------------------------------------------

            for row in rows:

                try:

                    # DATE
                    date = row.find_element(
                        By.CSS_SELECTOR,
                        "div.jackpot-event-row__date"
                    ).text.strip()


                    # TEAMS / GAME
                    teams = row.find_element(
                        By.CSS_SELECTOR,
                        "div.jackpot-event-row__event-name"
                    ).text.strip()


                    # RESULT
                    # Gets ONLY the second span
                    # Example: 3:2
                    result = row.find_element(
                        By.CSS_SELECTOR,
                        "div.jackpot-event-row__result span:nth-child(2)"
                    ).text.strip()


                    # OUTCOME
                    # Gets ONLY the second span
                    # Example: Home
                    outcome = row.find_element(
                        By.CSS_SELECTOR,
                        "div.jackpot-event-row__winning-pick span:nth-child(2)"
                    ).text.strip()


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

                    # Force the data to be written immediately
                    csv_file.flush()


                    # -------------------------------------------------
                    # PRINT WHAT WAS SAVED
                    # -------------------------------------------------

                    print(
                        f"Saved:"
                        f" {date} |"
                        f" {teams} |"
                        f" {result} |"
                        f" {outcome} |"
                        f" {link}"
                    )


                except Exception as e:

                    print(
                        f"Could not extract event: {e}"
                    )


            # -------------------------------------------------
            # ADD LINK TO EXISTING LINKS
            # -------------------------------------------------

            existing_links.add(link)


            print("-" * 60)
            print("Current page saved.")


        print("-" * 60)
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

        time.sleep(2)

        print("NEXT clicked.")

        time.sleep(2)


        # -------------------------------------------------
        # WAIT FOR NEW CONTENT
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
