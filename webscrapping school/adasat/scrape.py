import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a service object and specify the geckodriver path
service = Service('./geckodriver')  # Ensure 'geckodriver' is in the same directory as this script

# Create a new instance of Firefox WebDriver with options for better performance
options = webdriver.FirefoxOptions()
#options.add_argument('--headless')  # Run in headless mode if you don't need a browser UI
driver = webdriver.Firefox(service=service, options=options)

# Open the specified URL
driver.get('https://adasat.online/kw-en/product-list&types=&brand=&color=&collections=&replacement_list_id=&star_list_id=&sortby=4')

# Function to scroll to the bottom of the page until no new content loads
def scroll_until_no_new_content(driver, wait_time=3, max_scrolls=350, attempts_before_stop=5):
    last_product_count = 0
    scroll_attempts = 0
    stop_attempts = 0

    while scroll_attempts < max_scrolls and stop_attempts < attempts_before_stop:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)  # Wait for new content to load

        try:
            # Wait until the product list is present
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.ID, 'Productlist'))
            )
        except Exception as e:
            print(f"Waiting for product list timed out: {e}")
            break

        # Find all product items
        try:
            product_ul = driver.find_element(By.CSS_SELECTOR, 'div#Productlist div.product-list.clearfix ul.clearfix.productlistul')
            product_items = product_ul.find_elements(By.CLASS_NAME, 'productli')
            current_product_count = len(product_items)
            print(f"Current product count: {current_product_count}")
        except Exception as e:
            print(f"Error finding product items: {e}")
            break

        if current_product_count > last_product_count:
            last_product_count = current_product_count
            scroll_attempts += 1
            stop_attempts = 0  # Reset stop attempts since new products are loaded
            print("New products loaded. Continuing to scroll...")
        else:
            stop_attempts += 1
            print(f"No new products loaded. Attempt {stop_attempts}/{attempts_before_stop}")

    if scroll_attempts == max_scrolls:
        print("Reached maximum scroll attempts.")
    elif stop_attempts == attempts_before_stop:
        print("No new content loaded after multiple attempts. Stopping scroll.")

# Scroll until all content is loaded
scroll_until_no_new_content(driver)

# Open a CSV file to write the data
with open('product_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['Product Name', 'Product Link', 'Product Price'])

    try:
        # Wait for the product list to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'Productlist')))
        
        # Navigate to the main container div with id 'Productlist'
        product_list_div = driver.find_element(By.ID, 'Productlist')

        # Find the specific div with class 'product-list clearfix'
        product_list = product_list_div.find_element(By.CSS_SELECTOR, 'div.product-list.clearfix')

        # Locate the ul element with class 'clearfix productlistul' within the 'product-list clearfix' div
        product_ul = product_list.find_element(By.CSS_SELECTOR, 'ul.clearfix.productlistul')

        # Find all li elements with class 'productli' inside the ul
        product_items = product_ul.find_elements(By.CLASS_NAME, 'productli')

        print(f"Total products to collect: {len(product_items)}")

        # Initialize an empty set to keep track of collected product links
        collected_links = set()

        # Iterate through each product item and collect the necessary details
        for index, item in enumerate(product_items, start=1):
            try:
                # Ensure the 'product-box' div is visible
                product_box = WebDriverWait(item, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'product-box'))
                )

                # Inside 'product-box', find the div with class 'product-text clearfix'
                product_text = product_box.find_element(By.CSS_SELECTOR, 'div.product-text.clearfix')

                # Inside 'product-text clearfix', find the div with class 'product-name'
                product_name_div = product_text.find_element(By.CLASS_NAME, 'product-name')

                # Get the anchor tag within 'product-name' and extract the link and text
                product_anchor = product_name_div.find_element(By.TAG_NAME, 'a')
                product_link = product_anchor.get_attribute('href')
                product_name = product_anchor.text.strip()

                # Find the div with class 'product-price' inside 'product-text clearfix'
                product_price_div = product_text.find_element(By.CLASS_NAME, 'product-price')
                product_price = product_price_div.text.strip()

                # Check if this product link has already been collected
                if product_link and product_link not in collected_links:
                    collected_links.add(product_link)
                    # Print collected data
                    print(f"{index}. Product Name: {product_name}")
                    print(f"   Product Link: {product_link}")
                    print(f"   Product Price: {product_price}")
                    print('---')

                    # Write the collected data to the CSV file
                    writer.writerow([product_name, product_link, product_price])
            except Exception as e:
                print(f"Error retrieving product data for item {index}: {e}")

    except Exception as e:
        print(f"Error during data collection: {e}")

# Close the browser
driver.quit()
