import pandas as pd

# Load the CSV files
asn_descriptions_df = pd.read_csv('asn_descriptions.csv')
wemailweb_df = pd.read_csv('wemailweb.csv')

# Merge the DataFrames based on 'websites' in wemailweb_df and 'website' in asn_descriptions_df
merged_df = pd.merge(wemailweb_df, asn_descriptions_df[['website', 'asn_description']], 
                     left_on='websites', right_on='website', how='left')

# Display the first few rows of the merged DataFrame to confirm
print("Merged DataFrame:")
print(merged_df.head())
