import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Load the CSV file into a DataFrame
df = pd.read_csv('links.csv')

# Get the first 5 links
first_5_links = df['Link'].head(10)

# Setup Chrome WebDriver
service = Service('./chromedriver')  # Adjust the path if needed
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Step 1: Open the login page and wait for manual login
driver.get('https://www.pesarourbinolavoro.it/curriculum-candidati_1.html')
input("Please log in and press Enter here to continue...")

# Load existing data from 'collected_data.csv' if it exists
try:
    collected_df = pd.read_csv('collected_data.csv')
    existing_links = collected_df['Link'].tolist()
except FileNotFoundError:
    collected_df = pd.DataFrame()
    existing_links = []

# List to store the collected data
collected_data = []

# Step 2: Open each link and collect the 'Name', 'Residence', 'Email', and 'Phone'
for link in first_5_links:
    if link in existing_links:
        print(f"Skipping {link}, already collected.")
        continue
    
    driver.get(link)
    
    try:
        # Wait for the page to load and for the div with class 'col-sm-7' to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-7'))
        )
        
        # Locate the first div with class 'col-sm-7'
        div = driver.find_element(By.CLASS_NAME, 'col-sm-7')

        # Find the first h1 tag and extract the name
        h1 = div.find_element(By.TAG_NAME, 'h1')
        name = h1.text
        
        # Find the first h4 tag and extract the residence between <br> tags
        h4 = div.find_element(By.TAG_NAME, 'h4')
        h4_text = h4.text  # Get the text (which strips out all tags)

        # Split the text by newlines (as Selenium would have converted <br> tags to newlines)
        h4_lines = h4_text.split('\n')

        # Extract the residence text (the second line, which is between the first and second <br>)
        if len(h4_lines) > 1:
            residence = h4_lines[1].strip()
        else:
            residence = 'N/A'

        # Locate the div with class 'col-sm-9' and extract the phone and email
        div_contact = driver.find_element(By.CLASS_NAME, 'col-sm-9')

        # Find the first two <p> tags for email and phone
        contact_p_tags = div_contact.find_elements(By.TAG_NAME, 'p')
        
        if len(contact_p_tags) >= 2:
            email = contact_p_tags[0].text
            phone = contact_p_tags[1].text
        else:
            email = phone = 'N/A'

    except NoSuchElementException:
        name = 'N/A'
        residence = 'N/A'
        email = 'N/A'
        phone = 'N/A'

    # Append the collected data to the list
    collected_data.append({'Link': link, 'Name': name, 'Residence': residence, 'Email': email, 'Phone': phone})

# Step 3: Close the driver when done
driver.quit()

# Convert collected data to a DataFrame
new_collected_df = pd.DataFrame(collected_data)

# Append new data to the existing CSV file or create a new one
if not collected_df.empty:
    collected_df = pd.concat([collected_df, new_collected_df], ignore_index=True)
else:
    collected_df = new_collected_df

# Write the updated DataFrame to a CSV file
collected_df.to_csv('collected_data.csv', index=False)

# Optionally print the DataFrame
print(collected_df)
