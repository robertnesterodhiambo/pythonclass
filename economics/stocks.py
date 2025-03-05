import os
import pandas as pd
import yfinance as yf
import pymysql
from datetime import datetime

# Load the CSV data
#stock = pd.read_csv("~/GIT/Data/stock_details_5_years.csv")

stock = pd.read_csv("/home/dragon/.cache/kagglehub/datasets/iveeaten3223times/massive-yahoo-finance-dataset/versions/2/stock_details_5_years.csv")

# Get the unique company symbols
stock_list = stock['Company'].unique()

# Initialize an empty list to store the stock data
stock_data_list = []

# Define the date range
start_date = "2018-12-31"
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

# MySQL connection details
def get_db_connection():
    return pymysql.connect(
        host="localhost",  # Local MySQL server
        database="Stocks",  # The database name
        user="root",  # MySQL username
        password="1234",  # MySQL password
        port=3306  # Default MySQL port
    )

# Function to insert data into MySQL in chunks
def insert_data_in_chunks(csv_file, chunk_size=1000):
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the 'Stocks' table exists
        cursor.execute("""
            SHOW TABLES LIKE 'Stocks';
        """)
        table_exists = cursor.fetchone()

        # If table does not exist, create it
        if not table_exists:
            cursor.execute("""
                CREATE TABLE Stocks (
                    Date DATE,
                    Open FLOAT,
                    High FLOAT,
                    Low FLOAT,
                    Close FLOAT,
                    Volume INT,
                    AdjClose FLOAT,
                    Symbol VARCHAR(10)
                );
            """)
            print("Table 'Stocks' created.")
        else:
            print("Table 'Stocks' already exists.")

        # Read the CSV in chunks and insert data
        for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
            # Rename 'Adj Close' to 'AdjClose' only for insertion into MySQL
            chunk.rename(columns={"Adj Close": "AdjClose"}, inplace=True)

            # Insert each row in the chunk
            for _, row in chunk.iterrows():
                cursor.execute("""
                    INSERT INTO Stocks (Date, Open, High, Low, Close, Volume, AdjClose, Symbol)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row['Date'],
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume'],
                    row['AdjClose'],
                    row['Symbol']
                ))

            # Commit after each chunk
            connection.commit()
            print(f"Inserted {len(chunk)} rows into the 'Stocks' table.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Insert the data from the CSV file in chunks
insert_data_in_chunks("sample.csv", chunk_size=1000)

# Print the first few rows of the combined DataFrame
print(combined_df.head())

# Optionally, display the current working directory
print(os.getcwd())
