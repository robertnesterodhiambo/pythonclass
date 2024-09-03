import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Load the CSV file
df = pd.read_csv('completed_data.csv')

# Get the first 5 product links
product_links = df['Product Link'].head(5)

# Provide the relative path to GeckoDriver
gecko_path = os.path.join(os.getcwd(), 'geckodriver')

# Loop through each link and open it in a new WebDriver instance
for count, link in enumerate(product_links, start=1):
    try:
        # Setup a new Firefox WebDriver for each link
        service = Service(gecko_path)
        options = webdriver.FirefoxOptions()
        #options.add_argument('--headless')  # Run in headless mode if you don't want to open the browser window
        driver = webdriver.Firefox(service=service, options=options)
        
        # Open the link
        driver.get(link)
        
        # Wait until the div with class "submit-btn cart-btn notify_me" is present
        div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.submit-btn.cart-btn.notify_me"))
        )
        
        # Within that div, find the button and click it
        button = div.find_element(By.TAG_NAME, 'button')  # Assuming it's a button element
        button.click()
        print(f"Link {count} opened and button clicked: {link}")
        
    except Exception as e:
        print(f"An error occurred while processing link {count}: {e}")
    
    finally:
        # Ensure the browser is closed even if there's an error
        driver.quit()
