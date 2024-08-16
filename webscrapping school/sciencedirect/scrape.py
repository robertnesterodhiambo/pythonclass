import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
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

# Iterate through all links in the 'Link' column of the initial Excel file
for i, link in enumerate(df['Link']):
    if link in existing_links:
        print(f"Link {i + 1} already scraped, skipping.")
        continue  # Skip already scraped links
    
    try:
        # Initialize the WebDriver
        driver = initialize_driver()
        print(f"Opening link {i + 1}: {link}")  # Print the current link number
        driver.get(link)
        time.sleep(5)  # Pause for 5 seconds to let the page load fully

        # Locate the div with id="author-group"
        author_group_div = driver.find_element(By.ID, "author-group")

        # Find all buttons within the div with the specified classes
        buttons = author_group_div.find_elements(By.CSS_SELECTOR, ".button-link.button-link-secondary.button-link-underline")
        
        # Collect authors and their affiliations
        for button in buttons:
            author_text = button.text  # Store the text on the button as the author
            button.click()
            time.sleep(3)  # Pause to allow the side panel to open
            
            # Locate the side panel content
            side_panel_content = driver.find_element(By.CLASS_NAME, "side-panel-content")
            
            # Locate the div with class="affiliation" within the side panel
            affiliation_div = side_panel_content.find_element(By.CLASS_NAME, "affiliation")
            affiliation_text = affiliation_div.text  # Collect the text as the affiliation
            
            # Append the new data to the collected DataFrame
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
