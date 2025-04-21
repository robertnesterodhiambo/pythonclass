import pandas as pd

# Path to your Excel file
file_path = '/home/dragon/Documents/extracted_unit_numbers.xlsx'

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Display the first few rows
print(df.head())

