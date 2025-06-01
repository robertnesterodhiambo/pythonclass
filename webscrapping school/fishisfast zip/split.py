import pandas as pd

# Load the CSV
df_shipping = pd.read_csv("shipping_data.csv")

# Set display options for full output
pd.set_option('display.max_rows', None)        # Show all rows
pd.set_option('display.max_columns', None)     # Show all columns
pd.set_option('display.max_colwidth', None)    # Don't truncate text in cells
pd.set_option('display.expand_frame_repr', False)  # Don't break wide frames into multiple lines

# Print the full DataFrame
print(df_shipping.head())
