import pandas as pd

# Load the CSV files
asn_descriptions_df = pd.read_csv('asn_descriptions.csv')
wemailweb_df = pd.read_csv('wemailweb.csv')

# Display the first few rows of each DataFrame to confirm loading
print("ASN Descriptions DataFrame:")
print(asn_descriptions_df.head())

print("\nWemailweb DataFrame:")
print(wemailweb_df.head())
