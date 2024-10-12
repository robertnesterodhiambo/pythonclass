import requests

API_KEY = '8efwA6BX5pDsYWdGS5o5PuNe1vItTAGB'
year = 2024
month = 1  # January

# URL for the NYT Archive API
url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json'
params = {
    'api-key': API_KEY
}

# Send a request to the NYT API
response = requests.get(url, params=params)
data = response.json()

if response.status_code == 200:
    articles = data['response']['docs']
    stock_articles = []

    # Filter articles that mention "stocks" in the headline or snippet
    for article in articles:
        headline = article['headline']['main'].lower()
        snippet = article.get('snippet', '').lower()  # Some articles may not have a snippet
        
        if 'stocks' in headline or 'stocks' in snippet:
            stock_articles.append(article)
    
    # Print filtered articles
    if stock_articles:
        for article in stock_articles:
            print(f"Title: {article['headline']['main']}")
            print(f"Published Date: {article['pub_date']}")
            print(f"URL: {article['web_url']}")
            print(f"Snippet: {article.get('snippet', 'No snippet available')}")
            print()
    else:
        print("No articles about stocks found for this period.")
else:
    print(f"Error: {response.status_code}")
