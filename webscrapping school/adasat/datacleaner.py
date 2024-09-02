import pandas as pd
import re

# Load the Excel and CSV files into DataFrames
updated_product_data_df = pd.read_excel('updated_product_data.xlsx')
completed_data_df = pd.read_csv('completed_data.csv')

# Function to convert the vertical list format to a comma-separated string
def convert_to_comma_separated(text):
    if isinstance(text, str):
        return ','.join(text.splitlines())
    return text

# Apply the conversion function to both 'Left Eye Text' and 'Right Eye Text' columns
updated_product_data_df['Left Eye Text'] = updated_product_data_df['Left Eye Text'].apply(convert_to_comma_separated)
updated_product_data_df['Right Eye Text'] = updated_product_data_df['Right Eye Text'].apply(convert_to_comma_separated)

# Function to process the 'Product Price' column
def process_price(price):
    if isinstance(price, str):
        # Check if the price has two prices and a discount
        if re.match(r'^KWD \d+\.\d{3}\n\d+\.\d{3}\n\d+% off$', price.strip()):
            # Split the price and remove 'KWD'
            parts = price.split('\n')
            sale_off_price = float(parts[0].replace('KWD ', ''))
            product_price = float(parts[1])
            return product_price, sale_off_price
        elif price.startswith('KWD'):
            # Remove 'KWD' and return the price
            return float(price.replace('KWD ', '')), None
    return price, None

# Apply the function to the 'Product Price' column and create a new 'Sale Off Price' column
completed_data_df[['Product Price', 'Sale Off Price']] = completed_data_df['Product Price'].apply(
    lambda x: pd.Series(process_price(x))
)

# Merge the two DataFrames on the 'Product Link' column
merged_df = pd.merge(completed_data_df, updated_product_data_df[['Product Link', 'Left Eye Text', 'Right Eye Text']], 
                     on='Product Link', how='left')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_data.csv', index=False)

print("Merged data with updated product prices has been saved to 'merged_data.csv'")
