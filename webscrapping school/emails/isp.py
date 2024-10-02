import os
import socket
from ipwhois import IPWhois
import pandas as pd

# Function to get ISP information from a domain
def get_isp(domain):
    try:
        # Get the IP address of the domain
        ip = socket.gethostbyname(domain)
        # Use IPWhois to get ISP information
        ip_info = IPWhois(ip)
        result = ip_info.lookup_whois()
        return result.get('asn_description', 'No ASN description')  # ISP information
    except Exception as e:
        return f"Error: {str(e)}"

# Step 1: Read the CSV file wemailweb.csv
df = pd.read_csv('wemailweb.csv')

# Step 2: Drop rows with missing 'websites'
df_cleaned = df.dropna(subset=['websites'])

# Step 3: If 'asn_descriptions.csv' exists, load it and skip websites with filled 'asn_description'
if os.path.exists('asn_descriptions.csv'):
    df_existing = pd.read_csv('asn_descriptions.csv')
    
    # Check if 'asn_description' exists in the DataFrame
    if 'asn_description' in df_existing.columns:
        # Filter out websites where 'asn_description' is not NaN
        filled_websites = df_existing.dropna(subset=['asn_description'])['website'].unique()
        # Filter out these websites from df_cleaned
        df_cleaned = df_cleaned[~df_cleaned['websites'].isin(filled_websites)]
        
        # Print the skipped websites
        print("Skipped websites (already have ASN descriptions):")
        for website in filled_websites:
            print(website)
else:
    df_existing = pd.DataFrame(columns=['website', 'asn_description'])  # Create an empty DataFrame if file doesn't exist

# Step 4: Get unique websites (up to 10) for processing
unique_websites = df_cleaned['websites'].unique()

# Step 5: Create a list to store the ISP information
isp_data = []

# Step 6: Collect ASN descriptions for each website and print progress
for website in unique_websites:
    isp_description = get_isp(website)
    isp_data.append({'website': website, 'asn_description': isp_description})
    # Print the website and its ASN description to show progress
    print(f"Website: {website}, ASN Description: {isp_description}")

    # Step 7: Save the current lookup result to the CSV file after each lookup
    temp_df = pd.DataFrame([{'website': website, 'asn_description': isp_description}])
    
    # Append to the existing CSV or create a new one
    temp_df.to_csv('asn_descriptions.csv', mode='a', header=not os.path.exists('asn_descriptions.csv'), index=False)

    # Print confirmation of the save
    print(f"Saved: Website: {website}, ASN Description: {isp_description}")

# Step 8: Create a new DataFrame with the results from the collected data
isp_df = pd.DataFrame(isp_data)

# Step 9: Append the newly collected data to the existing data
if not df_existing.empty:
    df_combined = pd.concat([df_existing, isp_df], ignore_index=True)
else:
    df_combined = isp_df  # If no existing data, just use the new data

# Step 10: Save the combined DataFrame back to the CSV file
df_combined.to_csv('asn_descriptions.csv', index=False)

print("ASN descriptions saved successfully to 'asn_descriptions.csv'.")
