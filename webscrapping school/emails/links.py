import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
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
        # options.add_argument("--headless")  # Run in headless mode (optional)

        # Create a new instance of the Firefox driver
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

        try:
            # Open each link in the list
            for link in links_to_open:
                print(f"Opening: {link}")
                driver.get(link)
                time.sleep(5)  # Wait for the page to load

                # Scroll to the bottom of the page
                last_height = driver.execute_script("return document.body.scrollHeight")

                while True:
                    # Scroll down to the bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait for new content to load
                    time.sleep(3)  # Adjust time as necessary

                    # Calculate new scroll height and compare with last height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break  # Exit the loop if no new content has loaded
                    last_height = new_height

                # Find all spans with the class 'data'
                email_elements = driver.find_elements("css selector", "span.data a")

                # Initialize a list to store email data for this link
                emails_data = []

                # Extract email addresses from the found elements
                for element in email_elements:
                    email = element.get_attribute('href').replace('mailto:', '')  # Remove 'mailto:' from href

                    # Create a row of data for each email found
                    row_data = {
                        'Link': link,
                        'Email': email,  # Each email gets its own row
                    }

                    # Append original data from the first row to the row_data dictionary
                    for col in df.columns:
                        if col != 'Links':  # Exclude the 'Links' column to avoid duplicates
                            row_data[col] = df[col].iloc[0]  # Use the first row's data

                    emails_data.append(row_data)  # Append row data directly without checking for duplicates

                # Log the number of emails collected
                print(f"Collected {len(email_elements)} emails from {link}.")

                # Create a new DataFrame from the collected data for this link
                emails_df = pd.DataFrame(emails_data)

                # Append the new data to the existing emails DataFrame
                existing_emails_df = pd.concat([existing_emails_df, emails_df], ignore_index=True)

                # Save the combined data back to the CSV file
                existing_emails_df.to_csv('collected_emails.csv', index=False)
                
                # Print confirmation message
                print(f"Collected emails and data saved for {link}. Moving on to the next link...\n")

        finally:
            # Close the driver after opening the links
            driver.quit()

else:
    print("The 'Links' column is not found in the CSV file.")
