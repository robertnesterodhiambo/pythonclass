import pandas as pd

# Replace with the correct path if needed
file_path = "100 Country list 20180621.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Display the first few rows
print(df.head())
