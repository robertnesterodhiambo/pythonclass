import pandas as pd

# Load the CSV files
asn_descriptions_df = pd.read_csv('asn_descriptions.csv')
wemailweb_df = pd.read_csv('wemailweb.csv')

# Merge the DataFrames based on 'websites' in wemailweb_df and 'website' in asn_descriptions_df
merged_df = pd.merge(wemailweb_df, asn_descriptions_df[['website', 'asn_description']], 
                     left_on='websites', right_on='website', how='left')

# Drop the 'websites' column after merging
merged_df = merged_df.drop(columns=['websites'])

# Display the first few rows of the merged DataFrame to confirm
print("Merged DataFrame (with 'websites' dropped):")
print(merged_df.head())

# Save the merged DataFrame to a CSV file
merged_df.to_csv('merged.csv', index=False)

print("Merged DataFrame saved to 'merged.csv'.")
