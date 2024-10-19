import os
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = '8efwA6BX5pDsYWdGS5o5PuNe1vItTAGB'

# Step 1: Load the CSV and get unique stock symbols
file_path = '/root/Stock/sample.csv'
df = pd.read_csv(file_path)
unique_symbols = df['Symbol'].unique()

# Initialize an empty list to hold all stock-related articles
all_stock_articles = []

# Step 2: Get the current date and calculate the last 3 months
current_date = datetime.now()
last_3_months = [(current_date.year, current_date.month - i) if current_date.month - i > 0 
                 else (current_date.year - 1, current_date.month - i + 12) for i in range(3)]

# Step 3: Loop through each unique stock symbol and fetch articles from the last 3 months
for year, month in last_3_months:
    for symbol in unique_symbols:
        # URL for the NYT Archive API
        url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json'
        params = {
            'api-key': API_KEY
        }

        # Send a request to the NYT API
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data['response']['docs']
            
            # Filter articles that mention the current stock symbol in the headline or snippet
            for article in articles:
                headline = article['headline']['main'].lower()
                snippet = article.get('snippet', '').lower()  # Some articles may not have a snippet
                pub_date = article['pub_date'][:10]  # Extract only the date portion
                pub_date_dt = datetime.strptime(pub_date, '%Y-%m-%d')

                # Check if the stock symbol is mentioned in the headline or snippet
                if symbol.lower() in headline or symbol.lower() in snippet:
                    # Ensure the article was published in the last 3 months
                    if pub_date_dt >= current_date - timedelta(days=90):
                        stock_article = {
                            'Symbol': symbol,
                            'Title': article['headline']['main'],
                            'Published Date': article['pub_date'],
                            'URL': article['web_url'],
                            'Snippet': article.get('snippet', 'No snippet available')
                        }
                        all_stock_articles.append(stock_article)

        else:
            print(f"Error fetching data for {symbol} in {year}-{month}: {response.status_code}")

# Step 4: Save all the stock-related articles to a CSV file
if all_stock_articles:
    output_file = '/root/Stock/stock_articles_last_3_months.csv'
    # Convert the list of dictionaries to a DataFrame
    df_articles = pd.DataFrame(all_stock_articles)
    
    # Save to CSV
    df_articles.to_csv(output_file, index=False)
    print(f"Stock articles saved to {output_file}")
else:
    print("No articles about the stocks found.")
