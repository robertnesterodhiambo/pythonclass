import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load the CSV file
file_path = 'product_titles_and_links_with_pages.csv'
data = pd.read_csv(file_path)

# Set up the Firefox WebDriver
service = Service('./geckodriver')  # Make sure the geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Loop through the links and extract the product name
for index, row in data.iterrows():
    # Skip rows where 'productname2' is already filled
    if pd.notna(row['productname2']) and row['productname2'].strip() != '':
        print(f"Skipping link {row['product_link']} as 'productname2' is already filled.")
        continue

    try:
        driver.get(row['product_link'])
    except Exception as e:
        print(f"Failed to load link {row['product_link']}: {e}")
        data.at[index, 'productname2'] = 'URL Load Error'
        data.to_csv(file_path, index=False)
        continue

    try:
        # Explicitly wait for the h1 tag with the specific class to be present in the DOM
        product_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.h1.produtPage__title'))
        ).text
        # Save the extracted product name to the CSV data
        data.at[index, 'productname2'] = product_name
        print(f"Product Name Extracted: {product_name}")
    except Exception as e:
        print(f"Error occurred for link {row['product_link']}: {e}")
        data.at[index, 'productname2'] = 'Error'
        print(f"Saved as Error for link: {row['product_link']}")

    # Save the CSV after each iteration to avoid data loss
    data.to_csv(file_path, index=False)
    print(f"Data saved for link: {row['product_link']}")

# Close the browser
driver.quit()

# Final save to ensure all data is written
data.to_csv(file_path, index=False)
