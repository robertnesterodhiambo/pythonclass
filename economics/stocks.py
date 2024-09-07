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
start_date = "2024-09-05"
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

# Rename 'Adj Close' to 'AdjClose' only for insertion into SQLite
df_for_sql = combined_df.rename(columns={"Adj Close": "AdjClose"})

# Save the combined data to a CSV file
df_for_sql.to_csv("sample.csv", index=False)

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

# If table does not exist, create it with a primary key
if not table_exists:
    cursor.execute("""
        CREATE TABLE Stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    # Empty the table if it exists
    cursor.execute("DELETE FROM Stocks;")
    print("Table 'Stocks' cleared.")

# Define the chunk size for insertion
chunk_size = 1000  # Adjust the chunk size based on your needs

# Insert the data into the SQLite table in chunks
for start in range(0, len(df_for_sql), chunk_size):
    end = start + chunk_size
    df_for_sql.iloc[start:end].to_sql("Stocks", conn, if_exists='append', index=False, method='multi')

print("Data inserted into 'Stocks' table.")

# Commit the changes and close the connection
conn.commit()
conn.close()

# Print the first few rows of the combined DataFrame
print(combined_df.head())

# Optionally, display the current working directory
print(os.getcwd())
