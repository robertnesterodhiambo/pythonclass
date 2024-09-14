import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Load the CSV file into a DataFrame
df = pd.read_csv('links.csv')

# Get the first 5 links
first_5_links = df['Link'].head(5)

# Setup Chrome WebDriver
service = Service('./chromedriver')  # Adjust the path if needed
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# List to store the collected data
collected_data = []

# Open each link and collect the 'Name' and 'Residence'
for link in first_5_links:
    driver.get(link)
    time.sleep(3)  # Wait for the page to load

    try:
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

    except NoSuchElementException:
        name = 'N/A'
        residence = 'N/A'  # In case the element is not found

    # Append the collected data to the list
    collected_data.append({'Link': link, 'Name': name, 'Residence': residence})

# Close the driver when done
driver.quit()

# Convert collected data to a DataFrame and display it
collected_df = pd.DataFrame(collected_data)
print(collected_df)
