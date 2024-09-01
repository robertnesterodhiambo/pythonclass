import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file into a DataFrame
df = pd.read_csv('product_data.csv')

# Extract the first five links from the 'Product Link' column
links = df['Product Link'].head(5).tolist()

# Path to geckodriver in the same folder
geckodriver_path = './geckodriver'

# Define wait time in seconds
wait_time = 5  # Time to wait between opening browsers

# Initialize lists to store the product categories and image links
product_categories = []
image_links_list = []

# Open each link in a new Firefox driver instance
for link in links:
    # Set up the Firefox WebDriver
    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.add_argument('--start-maximized')

    # Initialize the WebDriver
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Open the link
        driver.get(link)
        print(f"Opened: {link}")

        # Wait for the product detail box to load
        wait = WebDriverWait(driver, 20)  # Maximum wait time of 20 seconds
        product_detail_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-detail-box')))

        # Extract the product category
        row = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))
        col = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-xs-12.col-sm-12.col-md-6')))
        product_details = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-details')))
        product_top_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-top-box')))
        brand_category = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'brand-category')))

        # Extract the text from the <p> tag
        product_category = brand_category.text
        product_categories.append(product_category)
        print(f"Product Category: {product_category}")

        # Extract all image links inside 'slick-list draggable'
        slick_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slick-list.draggable')))
        images = slick_list.find_elements(By.TAG_NAME, 'img')
        image_links = [img.get_attribute('src') for img in images]
        image_links_str = ', '.join(image_links)  # Join all image URLs into a single string
        image_links_list.append(image_links_str)
        print(f"Image Links: {image_links_str}")

    except Exception as e:
        print(f"An error occurred while processing {link}: {e}")
        product_categories.append(None)  # Add None if there is an error
        image_links_list.append(None)    # Add None if there is an error

    finally:
        # Close the WebDriver after processing
        driver.quit()

# Add the collected product categories and image links to the DataFrame
df['Product Category'] = pd.Series(product_categories)
df['Image Links'] = pd.Series(image_links_list)

# Save the updated DataFrame to a new CSV file
df.to_csv('completed_data.csv', index=False)
print("DataFrame has been saved to completed_data.csv")
