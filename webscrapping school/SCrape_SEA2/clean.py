import pandas as pd

# Load the CSV file
df = pd.read_csv("extracted_unit_numbers.csv")

# Drop rows where 'Unit Number' is 'Error' or blank/NaN
df_cleaned = df[~df['Unit Number'].isin(['Error', '', ' '])]
df_cleaned = df_cleaned.dropna(subset=['Unit Number'])

# Save back to the same file
df_cleaned.to_csv("extracted_unit_numbers.csv", index=False)

