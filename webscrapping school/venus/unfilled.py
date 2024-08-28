import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load the dataset
df = pd.read_csv('all_product_details.csv')

# Set up the Firefox WebDriver with options
options = Options()
#options.add_argument("--headless")  # Run in headless mode if you don't want the browser to open visibly
service = Service('./geckodriver')  # Ensure the geckodriver is in the same folder as this script

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Iterate over the first 5 product links
for i, row in df.iterrows():
    # Skip rows where 'product_name' is already filled
    if pd.notna(row['product_name']):
        print(f"Skipping row {i} as it is already filled.")
        continue
    
    link = row['product link']
    driver.get(link)
    
    try:
        # Wait for the div with class 'box-info-product' to be present
        div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'box-info-product'))
        )
        
        # Wait for the h1 tag with itemprop="name" inside the div to be present
        h1_element = WebDriverWait(div_element, 10).until(
            EC.presence_of_element_located((By.XPATH, './/h1[@itemprop="name"]'))
        )
        
        # Extract the text and store it in the DataFrame
        df.at[i, 'product_name'] = h1_element.text
        print(f"Collected product name: {h1_element.text}")
        
    except Exception as e:
        print(f"Failed to extract product name from {link}: {e}")
        df.at[i, 'product_name'] = 'N/A'
    
    # Save the DataFrame after each processed link
    df.to_csv('all_product_details.csv', index=False)
    print(f"Data saved after processing row {i}.")

# Close the WebDriver
driver.quit()
