import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Get the first link from the DataFrame
first_link = df.loc[0, 'Link']

# Set up the Firefox WebDriver (GeckoDriver)
service = Service('./geckodriver')  # Ensure the geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Open the first link in the browser
driver.get(first_link)

# Wait until the product list container is available
wait = WebDriverWait(driver, 10)
product_list_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product_list_container')))

# Find the ul with the class 'product_list row justify-content-center justify-content-sm-around'
product_list = product_list_container.find_element(By.CLASS_NAME, 'product_list.row.justify-content-center.justify-content-sm-around')

# Find all li elements with class 'ajax_block_product col-6 mb-2 mb-md-0 col-lg-3'
product_items = product_list.find_elements(By.CLASS_NAME, 'ajax_block_product.col-6.mb-2.mb-md-0.col-lg-3')

# Initialize an empty list to store the product links
product_links = []

# Iterate through each product item and extract the link
for product_item in product_items:
    try:
        # Wait for the anchor tag to be present
        anchor = WebDriverWait(product_item, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product_link'))
        )
        product_links.append(anchor.get_attribute('href'))
    except:
        print("Failed to retrieve the link for an item.")

# Store the collected links in a DataFrame
product_df = pd.DataFrame({'product link': product_links})

# Display the DataFrame (or you can save it to a CSV file)
print(product_df)

# Optionally, save to a CSV file
product_df.to_csv('product_links.csv', index=False)

# Close the browser
driver.quit()
