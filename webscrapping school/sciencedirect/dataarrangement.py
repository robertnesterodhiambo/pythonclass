import pandas as pd

# Load the Excel file into a DataFrame
file_path = 'ScienceDirect  Second LAST.xlsx'

df = pd.read_excel(file_path)

# Filter the DataFrame where the "Author" column is blank
blank_author_df = df[df['Author'].isna()]

# Filter the DataFrame where the "Author" column is not blank
non_blank_author_df = df.dropna(subset=['Author'])

# Group the non-blank DataFrame by 'Link', 'Author', and 'Affiliation'
grouped_df = non_blank_author_df.groupby(['Link', 'Author', 'Affiliation']).size().reset_index(name='count')

# Identify groups where the count is 1
unique_groups = grouped_df[grouped_df['count'] == 1]

# Merge these unique groups back with the blank_author_df based on the 'Link'
merged_df = pd.merge(blank_author_df, unique_groups[['Link', 'Author', 'Affiliation']], on='Link', how='left')

# Update the blank_author_df with the found 'Author' and 'Affiliation'
blank_author_df.update(merged_df)

# Replace the updated blank rows in the original DataFrame
df.update(blank_author_df)

# Save the updated DataFrame back to an Excel file
output_file_path = 'Updated_ScienceDirect.xlsx'
df.to_excel(output_file_path, index=False)

print("The DataFrame has been updated and saved as 'Updated_ScienceDirect.xlsx'")
