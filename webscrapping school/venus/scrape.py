import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Get the first link from the DataFrame
first_link = df.loc[0, 'Link']

# Set up the Firefox WebDriver (GeckoDriver)
service = Service('./geckodriver')  # Ensure the geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Open the first link in the browser
driver.get(first_link)

# Function to scrape data from the current page
def scrape_page():
    # Scroll to the bottom of the page to load all content
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for the page to load
        time.sleep(2)  # Adjust the sleep time as necessary

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Wait until the product list container is available
    wait = WebDriverWait(driver, 10)
    product_list_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product_list_container')))
    
    # Find the ul with the class 'product_list row justify-content-center justify-content-sm-around'
    product_list = product_list_container.find_element(By.CLASS_NAME, 'product_list.row.justify-content-center.justify-content-sm-around')
    
    # Find all li elements with class 'ajax_block_product col-6 mb-2 mb-md-0 col-lg-3'
    product_items = product_list.find_elements(By.CLASS_NAME, 'ajax_block_product.col-6.mb-2.mb-md-0.col-lg-3')
    
    # Initialize lists to store the product names and links
    product_names = []
    product_links = []
    
    # Iterate through each product item and extract the link and name
    for product_item in product_items:
        try:
            # Wait for the anchor tag to be present
            anchor = WebDriverWait(product_item, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product_link'))
            )
            product_links.append(anchor.get_attribute('href'))
            
            # Extract the product name
            product_name_span = product_item.find_element(By.CLASS_NAME, 'product_name.d-block')
            product_names.append(product_name_span.text)
        except Exception as e:
            print(f"Failed to retrieve details for an item: {e}")
    
    # Return the collected data
    return pd.DataFrame({'product name': product_names, 'product link': product_links})

# Initialize a variable to keep track of the page number
page_number = 1

# Loop to handle pagination
while True:
    # Scrape data from the current page
    page_df = scrape_page()
    
    # Save data to CSV file
    page_df.to_csv(f'product_details_page_{page_number}.csv', index=False)
    print(f"Data for page {page_number} saved.")

    try:
        # Locate and click the "Next" page link
        next_button = driver.find_element(By.ID, 'pagination_next').find_element(By.TAG_NAME, 'a')
        next_button.click()
        
        # Wait for the new page to load
        time.sleep(2)  # Adjust the sleep time as necessary
        
        # Increment the page number
        page_number += 1
    except Exception as e:
        print(f"No more pages or error occurred: {e}")
        break

# Close the browser
driver.quit()
