import pandas as pd
from selenium import webdriver
import time

# Load the CSV file
df = pd.read_csv('output_updated.csv')

# Get the first 5 links from the 'edit_link' column
links = df['edit_link'].head(5)

# Initialize the WebDriver (adjust the path to your WebDriver as needed)
driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH

# Open each link in a new tab and print the link number
for i, link in enumerate(links, start=1):
    print(f"Opening Link {i}: {link}")
    driver.get(link)
    time.sleep(2)  # Wait for 2 seconds to load the page

# Close the driver after the work is done
# driver.quit()  # Uncomment to close the browser when finished
