import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Load the Excel file
file_path = "data_final.xlsx"
df = pd.read_excel(file_path)

# Function to initialize the WebDriver
def initialize_driver():
    service = Service(executable_path="./geckodriver")  # Assuming geckodriver is in the same folder
    driver = webdriver.Firefox(service=service)
    return driver

# Lists to store the data
authors = []
affiliations = []
links = []

# Iterate through all links in the 'Link' column
for i, link in enumerate(df['Link']):
    try:
        # Initialize the WebDriver for each link
        driver = initialize_driver()
        print(f"Opening link {i + 1}")  # Print the current link number
        driver.get(link)
        time.sleep(5)  # Pause for 5 seconds to let the page load fully

        # Locate the div with id="author-group"
        author_group_div = driver.find_element(By.ID, "author-group")

        # Find all buttons within the div with the specified classes
        buttons = author_group_div.find_elements(By.CSS_SELECTOR, ".button-link.button-link-secondary.button-link-underline")
        
        # Click each button
        for button in buttons:
            author_text = button.text  # Store the text on the button as the author
            button.click()
            time.sleep(3)  # Pause to allow the side panel to open
            
            # Locate the side panel content
            side_panel_content = driver.find_element(By.CLASS_NAME, "side-panel-content")
            
            # Locate the div with class="affiliation" within the side panel
            affiliation_div = side_panel_content.find_element(By.CLASS_NAME, "affiliation")
            affiliation_text = affiliation_div.text  # Collect the text as the affiliation
            
            # Store the link, author, and affiliation
            links.append(link)
            authors.append(author_text)
            affiliations.append(affiliation_text)

    except Exception as e:
        print(f"Error processing link {i + 1}: {e}")
        links.append(link)
        authors.append("N/A")
        affiliations.append("N/A")
    
    finally:
        # Terminate the WebDriver after processing the link
        driver.quit()

# Combine the collected data into a DataFrame
output_df = pd.DataFrame({
    'Link': links,
    'Author': authors,
    'Affiliation': affiliations
})

# Save the output to an Excel file or CSV
output_file_path = "collected_data.xlsx"
output_df.to_excel(output_file_path, index=False)

print(f"Data collected and saved to {output_file_path}")
