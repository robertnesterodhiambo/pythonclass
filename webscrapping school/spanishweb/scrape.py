import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path to geckodriver
service = Service('./geckodriver')  # Ensure geckodriver is in the same folder as this script

# Initialize the Firefox WebDriver
driver = webdriver.Firefox(service=service)

# Open the desired URL
driver.get("https://www.pesarourbinolavoro.it/curriculum-candidati_1.html")

# Wait for the "ACCEDI" button to be clickable and then click it
try:
    accedi_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-warning"))
    )
    accedi_button.click()

    # Wait for the modal to appear and allow user to log in manually
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "modal-body"))
    )

    # Wait for the user to complete the login manually
    input("Please log in manually, then press Enter to reopen the page...")

    # Reopen the same URL after login is complete
    driver.get("https://www.pesarourbinolavoro.it/curriculum-candidati_1.html")

    # Scroll to the bottom to load all content
    SCROLL_PAUSE_TIME = 2  # Time to wait between scrolls
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Exit the loop when no more new content is loaded
        last_height = new_height

    # Find all divs with class "col-md-8 col-sm-6 listings"
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "col-md-8.col-sm-6.listings"))
        )
    except Exception as e:
        print(f"An error occurred while waiting for divs: {e}")

    # Find all divs with class "col-md-8 col-sm-6 listings"
    divs = driver.find_elements(By.CLASS_NAME, "col-md-8.col-sm-6.listings")

    if not divs:
        print("No divs with the specified class were found.")
    else:
        # Collect all nested links
        links = []
        for div in divs:
            # Find all anchor tags within the div (even if deeply nested)
            a_tags = div.find_elements(By.TAG_NAME, "a")
            for a_tag in a_tags:
                link = a_tag.get_attribute("href")
                if link:
                    links.append(link)

        # Write the links to a CSV file
        with open('links.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Link"])  # CSV header
            for link in links:
                writer.writerow([link])

        print(f"Collected {len(links)} links. Links have been written to links.csv.")

finally:
    # Close the driver after the task is completed
    input("Press Enter to close the browser...")
    driver.quit()
