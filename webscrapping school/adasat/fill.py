import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the existing CSV file into a DataFrame
df = pd.read_csv('completed_data.csv')

# Extract the first five links from the 'Product Link' column
links = df['Product Link'].tolist()

# Path to geckodriver in the same folder
geckodriver_path = './geckodriver'

# Define wait time in seconds
wait_time = 5  # Time to wait between opening browsers

# Open each link in a new Firefox driver instance
for i, link in enumerate(links):
    # Check if the 'Full Description' is already filled for the current entry
    if pd.notna(df.loc[i, 'Full Description']):
        print(f"Skipping already filled entry for link: {link}")
        continue

    # Set up the Firefox WebDriver
    service = Service(geckodriver_path)
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  
    options.add_argument('--start-maximized')

    # Initialize the WebDriver
    driver = webdriver.Firefox(service=service, options=options)

    try:
        # Open the link
        driver.get(link)
        print(f"Opened: {link}")

        # Scroll to the bottom of the page to ensure all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for the page to load after scrolling

        # Wait for the full description to load and extract its text
        wait = WebDriverWait(driver, 20)  # Maximum wait time of 20 seconds

        col_md_12 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-md-12')))
        info_div = col_md_12.find_element(By.CLASS_NAME, 'info')
        full_description = info_div.text
        df.loc[i, 'Full Description'] = full_description
        print(f"Full Description: {full_description}")

        # Wait for the product detail box to load
        product_detail_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'product-detail-box')))

        # Extract the product category
        brand_category = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'brand-category')))
        product_category = brand_category.text
        df.loc[i, 'Product Category'] = product_category
        print(f"Product Category: {product_category}")

        # Extract all image links and anchor links inside 'slick-list draggable'
        slick_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'slick-list.draggable')))
        
        # Extract image URLs from <img> tags within 'slick-list draggable'
        images = slick_list.find_elements(By.TAG_NAME, 'img')
        image_links = [img.get_attribute('src') for img in images]

        # Extract links from <a> tags inside 'slick-list draggable'
        anchors = slick_list.find_elements(By.TAG_NAME, 'a')
        anchor_links = [anchor.get_attribute('href') for anchor in anchors if anchor.get_attribute('href') != 'javascript:void(0)']

        # Combine image and anchor links into one list
        all_links = image_links + anchor_links
        all_links_str = ', '.join(all_links)  # Join all URLs into a single string
        df.loc[i, 'Image & Anchor Links'] = all_links_str
        print(f"Image & Anchor Links: {all_links_str}")

    except Exception as e:
        print(f"An error occurred while processing {link}: {e}")
        df.loc[i, 'Product Category'] = None  # Add None if there is an error
        df.loc[i, 'Image & Anchor Links'] = None  # Add None if there is an error
        df.loc[i, 'Full Description'] = None  # Add None if there is an error

    finally:
        # Close the WebDriver after processing
        driver.quit()

    # Save the updated DataFrame to a CSV file after each link
    df.to_csv('completed_data.csv', index=False)
    print(f"DataFrame saved to completed_data.csv after processing link {i + 1}")

print("All links have been processed and saved.")
