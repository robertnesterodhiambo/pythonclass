import requests
import csv
from datetime import datetime, timedelta

# API Key
API_KEY = 'ee36978344fe4a29be824bf2906e2903'

# Parameters for the API request
query = 'tesla'
from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
url = 'https://newsapi.org/v2/everything'

# Set up the parameters for the GET request
params = {
    'q': query,               # Search query for news about Tesla
    'from': from_date,       # Start date for articles
    'sortBy': 'publishedAt',  # Sort articles by publication date
    'apiKey': API_KEY         # Your API key
}

# Send the GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Define the CSV file name
    csv_file = f'tesla_news_{from_date}.csv'
    
    # Open the CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(['Published At', 'Source', 'Headline', 'URL', 'Content'])
        
        # Write each article's details
        for article in data['articles']:
            writer.writerow([
                article['publishedAt'],   # Published date
                article['source']['name'],  # Source of the news
                article['title'],          # Headline
                article['url'],            # URL to the full article
                article.get('content', '')  # Content (if available)
            ])
    
    print(f"Tesla news successfully saved to {csv_file}")
else:
    print(f"Failed to fetch news: {response.status_code}, {response.text}")
