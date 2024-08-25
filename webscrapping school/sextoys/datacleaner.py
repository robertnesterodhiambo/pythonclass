import pandas as pd

# Load the CSV file
file_path = 'product_titles_and_links_with_pages.csv'
df = pd.read_csv(file_path)

# Drop all rows with missing values
df_cleaned = df.dropna()

# Extract the numbers before .html and create a new column 'EABN'
df_cleaned['EABN'] = df_cleaned['product_link'].str.extract(r'(\d+)\.html')

# Select the first 10,000 rows
df_first_10000 = df_cleaned.iloc[:10000]

# Save the first 10,000 rows to an Excel file
output_file_path = 'cleaned_product_titles_and_links_first_10000_with_EABN.xlsx'
df_first_10000.to_excel(output_file_path, index=False)

print(f"First 10,000 rows of cleaned data with EABN saved to {output_file_path}")
