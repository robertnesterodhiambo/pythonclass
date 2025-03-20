import pandas as pd

# Load the CSV file
file_path = "extracted_data.csv"
df = pd.read_csv(file_path)

# Ensure column names are stripped of extra spaces
df.columns = df.columns.str.strip()

# Extract first name, middle name, last name, and position
df[['First Name', 'Middle Name', 'Last Name', 'Position']] = df['Full Name'].str.extract(
    r'^([\w.-]+)\s+((?:[\w.-]+\s+)+)?([\w-]+),\s*([\w.]+)?'
)

# Fill missing values for Middle Name and Position
df['Middle Name'] = df['Middle Name'].fillna("").str.strip()
df['Position'] = df['Position'].fillna("").str.strip()

# Create Full Name column without the position
df['Full Name (No Position)'] = df[['First Name', 'Middle Name', 'Last Name']].apply(
    lambda x: ' '.join(x.fillna('').astype(str)).strip(), axis=1
)

# Ensure 'Final' column exists before processing
if 'Final' in df.columns:
    # Extract street address, city, state, ZIP code, and miles
    address_pattern = r'\(\d{3}\)\s*\d{3}-\d{4}\s*\|\s*(.+?),\s*([A-Za-z\s-]+),\s*([A-Z]{2})\s*(\d{5})\s*\|\s*([\d.]+\s*miles)?'

    extracted_data = df['Final'].str.extract(address_pattern)

    # Assign extracted data to new columns
    df['Street Address'] = extracted_data[0].str.strip()
    df['City'] = extracted_data[1].str.strip()
    df['State'] = extracted_data[2].str.strip()
    df['ZIP Code'] = extracted_data[3].str.strip()
    df['Miles'] = extracted_data[4].fillna("").str.strip()  # Handle missing miles

else:
    print("Column 'Final' not found in the dataset!")

# Display cleaned data
print(df[['Full Name', 'First Name', 'Middle Name', 'Last Name', 'Position', 'Street Address', 'City', 'State', 'ZIP Code', 'Miles']].head())

# Save to CSV
df.to_csv("cleaned_extracted_data.csv", index=False)
