# Install required libraries
#!pip install requests beautifulsoup4

# Import libraries
import requests
from bs4 import BeautifulSoup

# URL of the webpage to scrape
url = 'https://www.agedcarequickstart.com.au/'

# Send a GET request to the webpage
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the page title
page_title = soup.title.string

# Print the page title
print("Page Title:", page_title)
