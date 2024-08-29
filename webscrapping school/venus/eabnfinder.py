import pandas as pd
import re

# Specify the path to your CSV file
file_path = 'all_product_details.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Function to extract the number from the product link
def extract_number(link):
    match = re.search(r'(\d+)\.html$', link)
    return match.group(1) if match else None

# Apply the function to the 'product link' column and create the 'EAB' column
df['EAB'] = df['product link'].apply(extract_number)

# Save the updated DataFrame back to the CSV file
df.to_csv(file_path, index=False)

print("Updated CSV file with 'EAB' column has been saved.")
