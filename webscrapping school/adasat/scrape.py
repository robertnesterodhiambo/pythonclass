import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a service object and specify the geckodriver path
service = Service('./geckodriver')  # Ensure 'geckodriver' is in the same directory as this script

# Create a new instance of Firefox WebDriver
driver = webdriver.Firefox(service=service)

# Open the specified URL
driver.get('https://adasat.online/kw-en/product-list&types=&brand=&color=&collections=&replacement_list_id=&star_list_id=&sortby=4')

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new content to load

# Open a CSV file to write the data
with open('product_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Product Name', 'Product Link', 'Product Price'])

    # Initialize an empty set to keep track of collected product links
    collected_links = set()
    previous_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'Productlist')))
        
        # Navigate to the main container div with id 'Productlist'
        product_list_div = driver.find_element(By.ID, 'Productlist')

        # Find the specific div with class 'product-list clearfix'
        product_list = product_list_div.find_element(By.CLASS_NAME, 'product-list.clearfix')

        # Locate the ul element with class 'clearfix productlistul' within the 'product-list clearfix' div
        product_ul = product_list.find_element(By.CLASS_NAME, 'clearfix.productlistul')

        # Find all li elements with class 'productli' inside the ul
        product_items = product_ul.find_elements(By.CLASS_NAME, 'productli')

        # Iterate through each product item and collect the necessary details
        for item in product_items:
            try:
                # Ensure the 'product-box' div is visible
                product_box = WebDriverWait(item, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'product-box')))

                # Inside 'product-box', find the div with class 'product-text clearfix'
                product_text = product_box.find_element(By.CLASS_NAME, 'product-text.clearfix')

                # Inside 'product-text clearfix', find the div with class 'product-name'
                product_name_div = product_text.find_element(By.CLASS_NAME, 'product-name')

                # Get the anchor tag within 'product-name' and extract the link and text
                product_anchor = product_name_div.find_element(By.TAG_NAME, 'a')
                product_link = product_anchor.get_attribute('href')
                product_name = product_anchor.text

                # Find the div with class 'product-price' inside 'product-text clearfix'
                product_price_div = product_text.find_element(By.CLASS_NAME, 'product-price')
                product_price = product_price_div.text

                # Check if this product link has already been collected
                if product_link not in collected_links:
                    collected_links.add(product_link)
                    # Print collected data
                    print(f'Product Name: {product_name}')
                    print(f'Product Link: {product_link}')
                    print(f'Product Price: {product_price}')
                    print('---')

                    # Write the collected data to the CSV file
                    writer.writerow([product_name, product_link, product_price])
            except Exception as e:
                print(f"Error retrieving product data: {e}")

        # Scroll to the bottom of the page
        scroll_to_bottom(driver)

        # Check if we've reached the bottom of the page
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break  # No new content loaded, exit the loop
        previous_height = new_height

# Close the browser
driver.quit()
