import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Load the CSV file
df = pd.read_csv('completed_data.csv')

# Get the first 5 product links
product_links = df['Product Link'].head(5)

# Provide the relative path to GeckoDriver
gecko_path = os.path.join(os.getcwd(), 'geckodriver')

# List to store new data
new_data = []

# Create a new CSV file to store the processed data
output_csv = 'processed_data.csv'
if os.path.exists(output_csv):
    os.remove(output_csv)  # Remove the file if it exists

# Loop through each link and open it in a new WebDriver instance
for count, link in enumerate(product_links, start=1):
    try:
        # Setup a new Firefox WebDriver for each link
        service = Service(gecko_path)
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')  # Run in headless mode if you don't want to open the browser window
        driver = webdriver.Firefox(service=service, options=options)
        
        # Open the link
        driver.get(link)
        
        # Wait for the button to be clickable and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.submit-btn.cart-btn.notify_me"))
        ).click()
        
        # Wait for the divs to become visible after clicking the button
        lefteyepower_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "lefteyepower"))
        )
        righteyepower_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "righteyepower"))
        )
        
        # Extract text from the divs
        lefteyepower_text = lefteyepower_div.text
        righteyepower_text = righteyepower_div.text
        
        # Print the processed information
        print(f"Processed Link {count}:")
        print(f"Product Link: {link}")
        print(f"Left Eye Power: {lefteyepower_text}")
        print(f"Right Eye Power: {righteyepower_text}")
        print("-" * 40)
        
        # Add the data to the list
        new_data.append({
            'Product Link': link,
            'Left Eye Power': lefteyepower_text,
            'Right Eye Power': righteyepower_text
        })
        
        # Save the processed data to the CSV file immediately
        pd.DataFrame([new_data[-1]]).to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)
    
    except Exception as e:
        print(f"An error occurred while processing link {count}: {e}")
    
    finally:
        # Ensure the browser is closed even if there's an error
        driver.quit()

# Optionally, merge with the original DataFrame and save to a new file
df = pd.merge(df, pd.DataFrame(new_data), on='Product Link', how='left')
df.to_csv('updated_completed_data.csv', index=False)
