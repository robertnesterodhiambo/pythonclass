import pandas as pd

# Set options to display full DataFrame content
pd.set_option('display.max_columns', None)        # Show all columns
pd.set_option('display.max_rows', None)           # Show all rows (use with caution on large DataFrames)
pd.set_option('display.max_colwidth', None)       # Show full column content, no truncation
pd.set_option('display.expand_frame_repr', False) # Prevent wrapping of wide DataFrames

# Now load the file
file_path = '/home/dragon/DATA/shipping_data.csv'

df = pd.read_csv(
    file_path,
    delimiter=",",
    quotechar='"',
    on_bad_lines='skip',
    engine='python'
)

print(df.head())
