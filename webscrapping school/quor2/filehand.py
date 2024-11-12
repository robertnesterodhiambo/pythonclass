import pandas as pd

# Load the CSV data into a DataFrame
df = pd.read_csv('collected_data.csv')

# Display the first few rows of the dataframe to confirm it loaded correctly
print(df.head())
