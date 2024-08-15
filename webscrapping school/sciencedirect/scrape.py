import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Load the Excel file
file_path = "data_final.xlsx"
df = pd.read_excel(file_path)

# Initialize the Firefox WebDriver
service = Service(executable_path="./geckodriver")  # Assuming geckodriver is in the same folder
driver = webdriver.Firefox(service=service)

# Lists to store the data
authors = []
affiliations = []

try:
    # Open the first 5 links from the 'Link' column
    for i, link in enumerate(df['Link'].head(5)):
        driver.get(link)
        time.sleep(3)  # Pause for 3 seconds to let the page load
        
        # Locate the div with id="author-group"
        author_group_div = driver.find_element(By.ID, "author-group")
        
        # Find all buttons within the div with the specified classes
        buttons = author_group_div.find_elements(By.CSS_SELECTOR, ".button-link.button-link-secondary.button-link-underline")
        
        # Click each button
        for button in buttons:
            author_text = button.text  # Store the text on the button as the author
            button.click()
            time.sleep(2)  # Pause to allow the side panel to open
            
            # Locate the side panel content
            try:
                side_panel_content = driver.find_element(By.CLASS_NAME, "side-panel-content")
                
                # Locate the div with class="affiliation" within the side panel
                affiliation_div = side_panel_content.find_element(By.CLASS_NAME, "affiliation")
                affiliation_text = affiliation_div.text  # Collect the text as the affiliation
                
                # Store the author and affiliation
                authors.append(author_text)
                affiliations.append(affiliation_text)
            
            except Exception as e:
                print(f"Error locating affiliation or side panel content: {e}")
                authors.append(author_text)
                affiliations.append("N/A")  # Store "N/A" if affiliation is not found
            
            # Close the side panel (optional: depending on the website's structure, this step might be needed)
            # You can add code to close the panel if necessary

finally:
    # Close the browser after opening the links
    driver.quit()

# Combine the collected data into a DataFrame
output_df = pd.DataFrame({
    'Author': authors,
    'Affiliation': affiliations
})

# Save the output to an Excel file or CSV
output_file_path = "collected_data.xlsx"
output_df.to_excel(output_file_path, index=False)

print(f"Data collected and saved to {output_file_path}")
