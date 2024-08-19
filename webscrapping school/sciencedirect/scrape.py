import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Load the Excel file with links to be scraped
file_path = "data_final.xlsx"
df = pd.read_excel(file_path)

# Load the Excel file with already collected data
collected_file_path = "collected_data.xlsx"
try:
    collected_df = pd.read_excel(collected_file_path)
    existing_links = set(collected_df['Link'])  # Convert to set for faster lookup
except FileNotFoundError:
    # If the file does not exist, create an empty DataFrame and set
    collected_df = pd.DataFrame(columns=['Link', 'Author', 'Affiliation'])
    existing_links = set()

# Function to initialize the WebDriver in headless mode
def initialize_driver():
    options = Options()
    options.add_argument("--headless")  # Enforce headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration if present
    options.add_argument("--no-sandbox")  # Sandbox may cause issues, disable it
    service = Service(executable_path="/home/dragon/Git/pythonclass/webscrapping school/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    return driver

# Function to get author and affiliation data
def get_author_and_affiliation(driver, link):
    driver.get(link)
    time.sleep(5)  # Wait for the page to load

    author_data = []
    
    # Locate the div with id="author-group"
    author_group_div = driver.find_element(By.ID, "author-group")
    
    # Retrieve authors and affiliations directly within the page
    buttons = author_group_div.find_elements(By.CSS_SELECTOR, ".button-link.button-link-secondary.button-link-underline")
    for button in buttons:
        author_text = button.text
        button.click()
        time.sleep(3)
        side_panel_content = driver.find_element(By.CLASS_NAME, "side-panel-content")
        affiliation_div = side_panel_content.find_element(By.CLASS_NAME, "affiliation")
        affiliation_text = affiliation_div.text
        author_data.append((author_text, affiliation_text))
    
    # Retrieve authors and affiliations from the linked pages
    anchor_tags = author_group_div.find_elements(By.CSS_SELECTOR, ".anchor.anchor-secondary.anchor-underline")
    for anchor in anchor_tags:
        author_text = anchor.text
        anchor.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "institution-scopus-id.text-s.u-margin-m-bottom")))
        affiliation_div = driver.find_element(By.CLASS_NAME, "institution-scopus-id.text-s.u-margin-m-bottom")
        affiliation_text = affiliation_div.text
        author_data.append((author_text, affiliation_text))
        driver.back()  # Navigate back to the original page
        time.sleep(3)  # Wait for the page to reload

    return author_data

# Iterate through all links in the 'Link' column of the initial Excel file
for i, link in enumerate(df['Link']):
    if link in existing_links:
        print(f"Link {i + 1} already scraped, skipping.")
        continue  # Skip already scraped links
    
    try:
        # Initialize the WebDriver
        driver = initialize_driver()
        print(f"Opening link {i + 1}: {link}")  # Print the current link number
        
        # Get author and affiliation data
        author_data = get_author_and_affiliation(driver, link)
        
        # Append the new data to the collected DataFrame
        for author_text, affiliation_text in author_data:
            new_data = pd.DataFrame({'Link': [link], 'Author': [author_text], 'Affiliation': [affiliation_text]})
            collected_df = pd.concat([collected_df, new_data], ignore_index=True)
            
            # Save the updated collected data to the Excel file
            collected_df.to_excel(collected_file_path, index=False)
            print(f"Data for author '{author_text}' added.")

    except Exception as e:
        print(f"Error processing link {i + 1}: {e}")
        # Store N/A if there was an error, and save it to maintain the record
        new_data = pd.DataFrame({'Link': [link], 'Author': ["N/A"], 'Affiliation': ["N/A"]})
        collected_df = pd.concat([collected_df, new_data], ignore_index=True)
        collected_df.to_excel(collected_file_path, index=False)
    
    finally:
        # Terminate the WebDriver after processing the link
        driver.quit()

print(f"Data collection completed. All data saved to {collected_file_path}")
