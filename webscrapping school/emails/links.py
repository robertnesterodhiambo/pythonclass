import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import re
import time
import os

# Load the CSV file into a DataFrame
df = pd.read_csv('collected_links.csv')

# Load existing emails if the collected_emails.csv file exists
if os.path.exists('collected_emails.csv'):
    existing_emails_df = pd.read_csv('collected_emails.csv')
else:
    existing_emails_df = pd.DataFrame(columns=['Link', 'Email'])

# Get the already collected links
already_collected_links = existing_emails_df['Link'].unique()

# Check if the 'Links' column exists
if 'Links' in df.columns:
    # Get the first 5 links from the 'Links' column
    links_to_open = df['Links'].tolist()

    # Filter out links that have already been collected
    links_to_open = [link for link in links_to_open if link not in already_collected_links]

    if not links_to_open:
        print("All links have already been processed.")
    else:
        # Set up Firefox WebDriver options
        options = Options()
        options.add_argument("--headless")  # Run in headless mode (optional)

        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        # Initialize a list to store email data
        emails_data = []

        try:
            # Open each link in the list
            for link in links_to_open:
                print(f"Opening: {link}")
                driver.get(link)
                time.sleep(5)  # Wait for the page to load

                # Extract page source
                page_source = driver.page_source
                
                # Find all email addresses using a regex
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_source)

                # Create a row of data for each email found
                for email in emails:
                    row_data = {
                        'Link': link,
                        'Email': email,  # Each email gets its own row
                    }
                    
                    # Append original data from the first row to the row_data dictionary
                    for col in df.columns:
                        if col != 'Links':  # Exclude the 'Links' column to avoid duplicates
                            row_data[col] = df[col].iloc[0]  # Use the first row's data

                    emails_data.append(row_data)

                # Create a new DataFrame from the collected data
                emails_df = pd.DataFrame(emails_data)

                # Append the new data to the existing emails DataFrame
                all_emails_df = pd.concat([existing_emails_df, emails_df], ignore_index=True)

                # Save the combined data back to the CSV file
                all_emails_df.to_csv('collected_emails.csv', index=False)
                
                # Print confirmation message
                print(f"Collected emails and data saved for {link}. Moving on to the next link...\n")

                # Clear the emails_data list for the next link
                emails_data.clear()

        finally:
            # Close the driver after opening the links
            driver.quit()

else:
    print("The 'Links' column is not found in the CSV file.")
