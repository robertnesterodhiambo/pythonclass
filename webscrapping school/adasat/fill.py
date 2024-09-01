import pandas as pd

# Replace 'your_path' with the actual path to your CSV file, if it's not in the same directory
df = pd.read_csv('product_data.csv')

# Display the first few rows of the dataframe to verify it has been imported correctly
print(df.head())
