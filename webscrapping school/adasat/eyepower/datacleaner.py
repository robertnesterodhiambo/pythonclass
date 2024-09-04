import pandas as pd
import re
# Replace 'path_to_your_file' with the actual path to your completed_data.csv file
df = pd.read_csv('completed_data.csv')

# Function to clean and format each cell
def format_cell(value):
    if pd.notna(value):
        # Remove newline characters and replace with commas
        return ','.join(value.split('\n'))
    return value

# Function to split the Product Category into Category and Subcategory
def split_category(value):
    if pd.notna(value):
        parts = value.split('- ', 1)  # Split into two parts at ' - '
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return parts[0], ''  # Handle case where there's no ' - '
    return '', ''

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
    return None, None  # Return None if the price doesn't match any known pattern

# Apply the process_price function to the Product Price column and create new columns
df[['Product Price', 'Sale Price']] = df['Product Price'].apply(process_price).apply(pd.Series)

#

# Apply the format_cell function to 'Left Eye Power' and 'Right Eye Power' columns
df['Left Eye Power'] = df['Left Eye Power'].apply(format_cell)
df['Right Eye Power'] = df['Right Eye Power'].apply(format_cell)

# Apply the split_category function to the Product Category column and create new columns
df[['Product Category', 'Product Subcategory']] = df['Product Category'].apply(split_category).apply(pd.Series)



# Display the first few rows of the DataFrame to confirm changes
print(df.head())

# Optionally, save the updated DataFrame to a new CSV file
df.to_csv('updated_data.csv', index=False)
