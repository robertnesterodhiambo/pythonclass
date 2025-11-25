import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os

# Path to the geckodriver executable
geckodriver_path = './geckodriver'

# Load the Excel file
file_path = 'C:\Users\Dragon\Documents\Github\pythonclass\webscrapping school\sextoys\navigation_links.xlsx'
df = pd.read_excel(file_path)

# Ensure the 'link' column exists in the DataFrame
if 'link' not in df.columns:
    raise ValueError("The DataFrame does not contain a 'link' column.")

# Set up Firefox WebDriver
options = Options()
options.headless = False  # Set to True if you don't need a visible browser window
service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Function to scroll to the bottom of the page
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Function to navigate to the next page
def go_to_next_page():
    try:
        # Wait until the "next" button with rel="next" is present
        wait_time = 10  # seconds
        start_time = time.time()
        while True:
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"].next.js-search-link')
                # Scroll the element into view
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)  # Wait for the scroll to take effect
                
                # Use JavaScript to click the button
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(5)  # Wait for the new page to load
                return True
            except Exception as e:
                if time.time() - start_time > wait_time:
                    print(f"Timeout or error navigating to next page: {e}")
                    return False
                time.sleep(1)  # Wait before retrying
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        return False

# Function to process each link
def process_link(link, file_handle):
    results = []
    driver.get(link)
    time.sleep(5)  # Wait for the page to load completely

    page_number = 1
    
    while True:
        print(f"Processing page {page_number} of {link}")
        
        # Scroll to the bottom of the page to load more results
        scroll_to_bottom()
        
        # Find all articles with the specified class
        try:
            article_elements = driver.find_elements(By.CSS_SELECTOR, 'article.product-miniature.js-product-miniature')
            
            if article_elements:
                for _ in range(len(article_elements)):  # Iterate over a copy of the list to handle stale elements
                    try:
                        # Re-fetch articles list
                        article_elements = driver.find_elements(By.CSS_SELECTOR, 'article.product-miniature.js-product-miniature')
                        article = article_elements[_]
                        
                        # Find the <h2> tag within the current article
                        h2_element = article.find_element(By.CSS_SELECTOR, 'h2.h3.product-title')
                        
                        # Extract the text of the <h2> tag
                        product_title = h2_element.text
                        
                        # Find the <a> tag inside the <h2> tag and extract the href attribute
                        a_tag = h2_element.find_element(By.TAG_NAME, 'a')
                        product_link = a_tag.get_attribute('href')
                        
                        # Append the result to the list
                        results.append({'link': link, 'page_number': page_number, 'product_title': product_title, 'product_link': product_link})
                        
                    except Exception as e:
                        if "stale element" in str(e).lower():
                            print(f"Stale element exception: {e}")
                            continue
                        print(f"Error extracting data from article in {link} on page {page_number}: {e}")
                        results.append({'link': link, 'page_number': page_number, 'product_title': "Not Found", 'product_link': "Not Found"})
            else:
                print(f"No articles found on page {page_number} of {link}")
                results.append({'link': link, 'page_number': page_number, 'product_title': "No Articles Found", 'product_link': "No Articles Found"})
        
        except Exception as e:
            print(f"Error processing page {page_number} of {link}: {e}")
            results.append({'link': link, 'page_number': page_number, 'product_title': "Error", 'product_link': "Error"})
        
        # Save results to CSV file after processing each page
        if results:
            results_df = pd.DataFrame(results)
            results_df.to_csv(file_handle, index=False, mode='a', header=file_handle.tell() == 0)
        
        # Check if there is a next page and go to it
        if not go_to_next_page():
            break
        
        page_number += 1

# Path to save the results
output_file_path = 'product_titles_and_links_with_pages.csv'

# Open file in append mode
with open(output_file_path, mode='w', newline='', encoding='utf-8') as file_handle:
    # Write header
    file_handle.write('link,page_number,product_title,product_link\n')
    
    # Iterate over each link and process it
    for index, row in df.iterrows():
        link = row['link']
        print(f"Starting processing for link: {link}")
        process_link(link, file_handle)
        print(f"Finished processing for link: {link}")

# Close the WebDriver
driver.quit()

print("Finished extracting product titles, links, and page numbers from all links.")
