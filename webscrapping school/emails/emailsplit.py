import pandas as pd

# Specify the file path
file_path = 'collected_emails.csv'

# Load the CSV file into a DataFrame
email_data = pd.read_csv(file_path)

# Split the 'Email' column and extract the part after '@' into a new column 'websites'
email_data['websites'] = email_data['Email'].str.split('@').str[1]

# Save the updated DataFrame to a new CSV file
output_file = 'wemailweb.csv'
email_data.to_csv(output_file, index=False)

# Display the first few rows of the updated DataFrame to confirm the new column is added
print(email_data.head())
