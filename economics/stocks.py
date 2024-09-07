import os
import pandas as pd
import yfinance as yf
import sqlite3
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

# Keep the original column names for the DataFrame
common_colnames = ["Date", "Open", "High", "Low", "Close", "Volume", "Adj Close", "Symbol"]
combined_df.columns = common_colnames

# Save the combined data to a CSV file
combined_df.to_csv("sample.csv", index=False)

# Path to SQLite file
db_file = "stock_data.db"

# If SQLite file doesn't exist, this line creates it automatically
conn = sqlite3.connect(db_file)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Check if the table 'Stocks' exists
cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table' AND name='Stocks';
""")
table_exists = cursor.fetchone()

# If table does not exist, create it
if not table_exists:
    cursor.execute("""
        CREATE TABLE Stocks (
            Date TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume INTEGER,
            AdjClose REAL,
            Symbol TEXT
        );
    """)
    print("Table 'Stocks' created.")
else:
    print("Table 'Stocks' already exists.")

# Rename 'Adj Close' to 'AdjClose' only for insertion into SQLite
df_for_sql = combined_df.rename(columns={"Adj Close": "AdjClose"})

# Insert the data into the SQLite table
df_for_sql.to_sql("Stocks", conn, if_exists='append', index=False)
print("Data inserted into 'Stocks' table.")

# Commit the changes and close the connection
conn.commit()
conn.close()

# Print the first few rows of the combined DataFrame
print(combined_df.head())

# Optionally, display the current working directory
print(os.getcwd())
