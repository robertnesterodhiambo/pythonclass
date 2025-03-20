import pandas as pd

# Load the CSV file
file_path = "extracted_data.csv"
df = pd.read_csv(file_path)

# Updated regex to support initials as first names, middle names, and hyphenated last names
df[['First Name', 'Middle Name', 'Last Name', 'Position']] = df['Full Name'].str.extract(
    r'^([\w.-]+)\s+((?:[\w.-]+\s+)+)?([\w-]+),\s*([\w.]+)?'
)


# Fill missing values for Middle Name and Position
df['Middle Name'] = df['Middle Name'].fillna("").str.strip()
df['Position'] = df['Position'].fillna("").str.strip()

# Create Full Name column without the position, handling NaN values properly
df['Full Name (No Position)'] = df[['First Name', 'Middle Name', 'Last Name']].apply(
    lambda x: ' '.join(x.fillna('').astype(str)).strip(), axis=1
)

# Display the cleaned data
print(df[['Full Name', 'First Name', 'Middle Name', 'Last Name', 'Full Name (No Position)', 'Position']].head())

# Save the cleaned data to a new CSV file
df.to_csv("cleaned_extracted_data.csv", index=False)
