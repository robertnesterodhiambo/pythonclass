import pandas as pd
import requests
import csv
import time
from datetime import datetime, timedelta

# API Key
API_KEY = 'ee36978344fe4a29be824bf2906e2903'

# Path to your CSV file
csv_path = '/home/dragon/GIT/Data/sample.csv'

# Read the CSV file to get the data
df = pd.read_csv(csv_path)

# Get the top 50 symbols based on the highest 'Adj Close' values
top_symbols = df.nlargest(50, 'Adj Close')['Symbol'].unique()

# Parameters for the API request
from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
url = 'https://newsapi.org/v2/everything'

# Define the CSV file name for all articles
output_csv_file = f'top_50_stock_news_{datetime.now().strftime("%Y%m%d")}.csv'

# Open the CSV file for writing
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Stock Symbol', 'Published At', 'Source', 'Headline', 'URL', 'Content'])

    # Fetch news for each of the top 50 stock symbols
    for stock in top_symbols:
        # Set up the parameters for the GET request
        params = {
            'q': stock,               # Search query for news about the stock
            'from': from_date,       # Start date for articles
            'sortBy': 'publishedAt',  # Sort articles by publication date
            'language': 'en',
            'apiKey': API_KEY         # Your API key
        }

        # Send the GET request to the API
        response = requests.get(url, params=params)

        # Log the response status and content for debugging
        print(f"Fetching news for {stock}: Status Code {response.status_code}")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()
            
            # Check if any articles were returned
            if data['totalResults'] > 0:
                # Write each article's details along with the stock symbol
                for article in data['articles']:
                    writer.writerow([
                        stock,                     # Stock Symbol
                        article['publishedAt'],    # Published date
                        article['source']['name'],  # Source of the news
                        article['title'],           # Headline
                        article['url'],             # URL to the full article
                        article.get('content', '')   # Content (if available)
                    ])
                
                print(f"News articles for {stock} successfully added to {output_csv_file}.")
            else:
                print(f"No articles found for {stock}.")
        else:
            print(f"Failed to fetch news for {stock}: {response.status_code}, {response.text}")

        # Add a delay to avoid hitting API rate limits
        time.sleep(1)  # Wait for 1 second before the next request

print(f"All stock news saved to {output_csv_file}.")
