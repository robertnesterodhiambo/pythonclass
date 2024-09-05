import pandas as pd
import yfinance as yf
from datetime import datetime

# Load the CSV data
stock = pd.read_csv("~/GIT/Data/stock_details_5_years.csv")

# Get the unique company symbols
stock_list = stock['Company'].unique()

# Initialize an empty list to store the stock data
stock_data_list = []

# Define the date range
start_date = "2023-12-12"
end_date = datetime.today()

# Loop through each symbol and download the data
for symbol in stock_list:
    try:
        # Download stock data for the current symbol
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        
        # Add a column for the stock symbol
        stock_data['Symbol'] = symbol
        
        # Reset the index to get 'Date' as a column
        stock_data.reset_index(inplace=True)
        
        # Append the DataFrame to the list
        stock_data_list.append(stock_data)
    except Exception as e:
        print(f"Error downloading data for {symbol}: {e}")

# Combine all the DataFrames into one
combined_df = pd.concat(stock_data_list, ignore_index=True)

# Define the common column names
common_colnames = ["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close", "Symbol"]

# Rename the columns to the common names
combined_df.columns = common_colnames

# Save the combined data to a CSV file
combined_df.to_csv("sample.csv", index=False)

# Print the first few rows of the combined DataFrame
print(combined_df.head())

# Optionally, you can display the current working directory
import os
print(os.getcwd())
