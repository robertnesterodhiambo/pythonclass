

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up Selenium WebDriver options for Firefox
options = webdriver.FirefoxOptions()
#
dr = webdriver.Firefox(options=options)

# Access the website for scraping
dr.get("https://www.geeksforgeeks.org/")  # Website used for scraping

# Display the title of the website
print(dr.title, "\n")

# Display some GFG's Articles
c = 1
for i in dr.find_elements(By.CLASS_NAME, 'gfg_home_page_article_meta'):
    print(str(c) + ". ", i.text)
    c += 1

# Import the CSV file
data = pd.read_csv('output.csv')

# Get the first 5 links from the 'Link' column
links = data['Link'].head(5)

# Function to scroll to the bottom of the page and check for text
def scroll_and_check_text(driver, search_text):
    last_height = driver.execute_script("return document.body.scrollHeight")
    found_text = False

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(2)  # Adjust sleep time as needed

        # Check if the desired text is present on the page
        page_source = driver.page_source
        if search_text in page_source:
            found_text = True
            break

        # Calculate new scroll height and compare with last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # If heights are the same, we are at the bottom
            break
        last_height = new_height

    return found_text

# Open each link in the browser using Selenium with '/log' appended
for idx, link in enumerate(links, 1):
    modified_link = link + '/log'  # Add '/log' to the link
    print(f"Opening link {idx}: {modified_link}")
    dr.get(modified_link)

    # Check for the text "User name edited by" as we scroll
    text_found = scroll_and_check_text(dr, "User name edited by")

    # Print result based on whether the text was found
    if text_found:
        print("yes edit")
    else:
        print("not edit")

# Quit the browser after opening all links
dr.quit()
