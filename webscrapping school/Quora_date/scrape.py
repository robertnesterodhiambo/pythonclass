import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Load the CSV file
df = pd.read_csv('merged_output.csv')

# Extract the first 5 links from the 'edit_link' column
edit_links = df['edit_link'].head(5)

# Set up the Chrome WebDriver
service = Service('./chromedriver')  # Adjust path if needed
driver = webdriver.Chrome(service=service)

def scroll_page(driver, times=5):
    """
    Scroll to the bottom of the page a specified number of times.
    """
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"Scrolled {i+1} time(s).")
        time.sleep(2)  # Wait for the page to load new content, adjust if needed

def extract_user_edited_text(driver):
    """
    Extract and print text from divs with class 'q-box' containing the phrase 'User name edited by'.
    """
    divs = driver.find_elements(By.CLASS_NAME, "q-box")
    for div in divs:
        text = div.text
        if "User name edited by" in text:
            print(f"Found: {text}")

try:
    # Step 1: Open Quora for login
    print("Opening Quora for login...")
    driver.get('https://www.quora.com/')
    
    # Wait for the user to log in
    input("Press Enter after logging in to Quora...")
    
    # Step 2: Open each link from the CSV, scroll, and extract data
    for link in edit_links:
        print(f"Opening: {link}")
        driver.get(link)
        
        # Scroll the page 5 times
        scroll_page(driver, times=5)
        
        # Extract and print relevant text
        extract_user_edited_text(driver)
        print(f"Finished processing {link}")
        
finally:
    # Close the browser after processing
    driver.quit()
