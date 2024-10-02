import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time

# Load the CSV file into a DataFrame
df = pd.read_csv('collected_links.csv')

# Check if the 'Links' column exists
if 'Links' in df.columns:
    # Get the first 5 links from the 'Links' column
    links_to_open = df['Links'].head(5).tolist()

    # Set up Firefox WebDriver options
    options = Options()
    #options.add_argument("--headless")  # Run in headless mode (optional)

    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    try:
        # Open each link in the list
        for link in links_to_open:
            print(f"Opening: {link}")
            driver.get(link)
            time.sleep(5)  # Wait for 5 seconds to let the page load (adjust as needed)

    finally:
        # Close the driver after opening the links
        driver.quit()
else:
    print("The 'Links' column is not found in the CSV file.")
