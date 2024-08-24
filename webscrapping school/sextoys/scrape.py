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

# Initialize a list to store the results
results = []

# Open each link from the DataFrame
for index, row in df.iterrows():
    link = row['link']
    print(f"Opening link: {link}")
    driver.get(link)
    time.sleep(5)  # Wait for 5 seconds to ensure the page loads completely
    
    # Find all articles with the specified class
    try:
        article_elements = driver.find_elements(By.CSS_SELECTOR, 'article.product-miniature.js-product-miniature')
        
        if article_elements:
            for article in article_elements:
                try:
                    # Find the <h2> tag within the current article
                    product_title_element = article.find_element(By.CSS_SELECTOR, 'h2.h3.product-title')
                    product_title = product_title_element.text
                    results.append({'link': link, 'product_title': product_title})
                except Exception as e:
                    print(f"Error extracting title from article in {link}: {e}")
                    results.append({'link': link, 'product_title': "Not Found"})
        else:
            print(f"No articles found in {link}")
            results.append({'link': link, 'product_title': "No Articles Found"})
    
    except Exception as e:
        print(f"Error processing {link}: {e}")
        results.append({'link': link, 'product_title': "Error"})

# Close the WebDriver
driver.quit()

# Convert results to a DataFrame and save to Excel
results_df = pd.DataFrame(results)
results_df.to_excel('product_titles.xlsx', index=False)

print("Finished extracting product titles.")
