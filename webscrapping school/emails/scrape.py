from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.by import By
import csv

# Set options for Firefox
options = Options()
# options.add_argument('--headless')  # Uncomment to run in headless mode (without opening a browser window)
options.add_argument('--disable-gpu')

# Set the path to the GeckoDriver executable
gecko_driver_path = './geckodriver'  # Assuming the GeckoDriver is in the same folder

# Initialize the Firefox driver with GeckoDriver
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service, options=options)

# Open the specified URL
url = 'https://ted.europa.eu/en/search/result?notice-type=can-standard%2Ccan-social%2Ccan-desg%2Ccan-tran&place-of-performance=DEU&search-scope=ACTIVE'
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Initialize page number
page_number = 1

# Open the CSV file for writing links
with open('collected_links.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Page Number', 'Links'])  # Write the header

    # Loop through the pages
    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for content to load after scrolling
        time.sleep(5)

        # Locate all <a> tags with the specified class
        links_elements = driver.find_elements(By.CSS_SELECTOR, 'a.css-q5fadx.ed8fupw0')

        # Extract the href attributes and store them in a list
        links = [element.get_attribute('href') for element in links_elements]

        # Write the collected links to the CSV file for the current page
        for link in links:
            writer.writerow([page_number, link])  # Write the page number and link

        print(f"Links from page {page_number} have been added to collected_links.csv.")

        # Check for the "Go to the next page" button and click it
        try:
            next_button = driver.find_element(By.XPATH, "//button[@aria-label='Go to the next page']")
            next_button.click()  # Click the next page button
            
            # Wait for the next page to load
            time.sleep(5)

            # Increment the page number
            page_number += 1
        except Exception as e:
            print("No more pages to load or an error occurred:", e)
            break  # Exit the loop if no next button is found

# Close the browser after use
driver.quit()
