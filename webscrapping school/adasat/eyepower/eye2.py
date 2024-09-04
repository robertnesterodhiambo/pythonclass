import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load the data
data = pd.read_csv('completed_data.csv')

# Add columns to store the eye power data if they don't exist already
if 'Left Eye Power' not in data.columns:
    data['Left Eye Power'] = ''
if 'Right Eye Power' not in data.columns:
    data['Right Eye Power'] = ''

# Set up the Firefox WebDriver
options = Options()
#options.add_argument('--headless')  # Run in headless mode if you don't want the browser to open visually
service = Service(executable_path='./geckodriver')  # Path to the GeckoDriver

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Loop through the first 5 links in the 'Product Link' column
for idx, row in data.iterrows():
    # Check if both Left Eye Power and Right Eye Power columns are filled
    if pd.notna(row['Left Eye Power']) and pd.notna(row['Right Eye Power']):
        print(f"Link {idx+1} already processed. Skipping...")
        continue

    link = row['Product Link']
    driver.get(link)  # Open the link in the browser
    print(f"Opened: {link}")
    
    try:
        # Wait for the page to load fully
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        
        # Scroll to the button to ensure it's in view
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.submit-btn.cart-btn.notify_me"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)  # Wait a bit to ensure scrolling completes
        
        # Attempt to click the button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.submit-btn.cart-btn.notify_me"))
        ).click()
        print("Button clicked successfully.")

        # Wait for the divs to become visible after clicking the button
        lefteyepower_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "lefteyepower"))
        )
        righteyepower_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "righteyepower"))
        )

        # Collect the text from the divs
        lefteyepower_text = lefteyepower_div.text
        righteyepower_text = righteyepower_div.text

        # Save the collected data into the DataFrame
        data.at[idx, 'Left Eye Power'] = lefteyepower_text
        data.at[idx, 'Right Eye Power'] = righteyepower_text

        print(f"Left Eye Power: {lefteyepower_text}")
        print(f"Right Eye Power: {righteyepower_text}")

        # Save the DataFrame back to the CSV file after each link
        data.to_csv('completed_data.csv', index=False)
        print(f"Data for link {idx+1} saved to 'completed_data.csv'.")

    except Exception as e:
        print(f"An error occurred with link {idx+1}: {e}")

    time.sleep(3)  # Wait for 3 seconds before moving to the next link

# Quit the WebDriver after processing all links
driver.quit()
