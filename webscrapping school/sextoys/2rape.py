import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file
file_path = 'product_titles_and_links_with_pages.csv'
data = pd.read_csv(file_path)

# Create a new column for the product names
data['productname2'] = ''

# Set up the Firefox WebDriver
service = Service('./geckodriver')  # Make sure the geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Loop through the first 5 links and extract the product name
for index, link in enumerate(data['product_link'].head()):
    driver.get(link)

    try:
        # Explicitly wait for the h1 tag with the specific class to be present in the DOM
        product_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.h1.produtPage__title'))
        ).text
        # Save the extracted product name to the CSV data
        data.at[index, 'productname2'] = product_name
        print(f"Product Name Extracted: {product_name}")
    except Exception as e:
        print(f"Error occurred for link {link}: {e}")
        data.at[index, 'productname2'] = 'Error'
        print(f"Saved as Error for link: {link}")

    # Save the CSV after each iteration to avoid data loss
    data.to_csv(file_path, index=False)
    print(f"Data saved for link: {link}")

# Close the browser
driver.quit()

# Final save to ensure all data is written
data.to_csv(file_path, index=False)
