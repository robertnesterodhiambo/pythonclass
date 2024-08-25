import pandas as pd

# Load the Excel file
file_path = 'product_titles_and_links_with_pages.xlsx'
df = pd.read_excel(file_path)

# Drop all rows with missing values
df_cleaned = df.dropna()

# Display the first 5 rows of the cleaned DataFrame
print(df_cleaned.head())
