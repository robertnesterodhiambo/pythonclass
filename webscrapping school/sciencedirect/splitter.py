import pandas as pd

# Load the Excel file
file_path = 'collected_data.xlsx'  # Update this with the correct path to your file
df = pd.read_excel(file_path)

# Split the 'Affiliation' column by commas
split_columns = df['Affiliation'].str.split(',', expand=True)

# Rename the split columns to 'Affiliation_1', 'Affiliation_2', ..., 'Affiliation_n'
num_splits = split_columns.shape[1]  # Number of new columns created
split_columns.columns = [f'Affiliation_{i+1}' for i in range(num_splits)]

# Concatenate the original DataFrame with the new split columns
df_split = pd.concat([df, split_columns], axis=1)

# Save the result back to an Excel file
df_split.to_excel('collected_data_split.xlsx', index=False)
