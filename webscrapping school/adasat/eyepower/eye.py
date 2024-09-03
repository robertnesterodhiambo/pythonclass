import pandas as pd

# Load the CSV file
df = pd.read_csv('completed_data.csv')

# Display the first 5 rows
first_five_rows = df.head()
print(first_five_rows)
