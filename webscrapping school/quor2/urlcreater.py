import pandas as pd

# Load the CSV file
df = pd.read_csv('output.csv')

# Create a new column 'edit_link' with '/log' added to each link in the 'Link' column
df['edit_link'] = df['Link'] + '/log'
df.to_csv('output_updated.csv', index=False)

# Display the updated DataFrame
print(df.head(10))
