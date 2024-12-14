from yahoo_fin import stock_info

def fetch_yahoo_finance_news_alt(ticker):
    try:
        # Fetch news for the ticker
        news = stock_info.get_news(ticker)
        
        # Format and display news articles
        articles = []
        for article in news:
            title = article.get('title', 'No title')
            link = article.get('link', '#')
            articles.append({"title": title, "link": link})
        
        return articles
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []

# Example usage
ticker = "AAPL"
news = fetch_yahoo_finance_news_alt(ticker)

print(f"News for {ticker}:")
for i, article in enumerate(news, start=1):
    print(f"{i}. {article['title']} - {article['link']}")
