import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

# Path to the geckodriver executable
geckodriver_path = './geckodriver'

# Load the Excel file
file_path = 'navigation_links.xlsx'
df = pd.read_excel(file_path)

# Ensure the 'link' column exists in the DataFrame
if 'link' not in df.columns:
    raise ValueError("The DataFrame does not contain a 'link' column.")

# Select only the first 2 rows
df = df.head(2)

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
        next_button = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"].next.js-search-link')
        if next_button:
            next_button.click()
            time.sleep(5)  # Wait for the new page to load
            return True
        else:
            return False
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        return False

# Initialize a list to store the results
results = []

# Open each link from the DataFrame
for index, row in df.iterrows():
    link = row['link']
    print(f"Opening link: {link}")
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
                for article in article_elements:
                    try:
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
                        print(f"Error extracting data from article in {link} on page {page_number}: {e}")
                        results.append({'link': link, 'page_number': page_number, 'product_title': "Not Found", 'product_link': "Not Found"})
            else:
                print(f"No articles found on page {page_number} of {link}")
                results.append({'link': link, 'page_number': page_number, 'product_title': "No Articles Found", 'product_link': "No Articles Found"})
        
        except Exception as e:
            print(f"Error processing page {page_number} of {link}: {e}")
            results.append({'link': link, 'page_number': page_number, 'product_title': "Error", 'product_link': "Error"})
        
        # Check if there is a next page and go to it
        if not go_to_next_page():
            break
        
        page_number += 1

# Close the WebDriver
driver.quit()

# Convert results to a DataFrame and save to Excel
results_df = pd.DataFrame(results)
results_df.to_excel('product_titles_and_links_with_pages.xlsx', index=False)

print("Finished extracting product titles, links, and page numbers.")
