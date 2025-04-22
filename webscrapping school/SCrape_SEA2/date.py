import pandas as pd
import re

# Load the Excel file
file_path = '/home/dragon/Documents/extracted_unit_numbers.xlsx'
df = pd.read_excel(file_path)

# Function to extract the date after the keyword
def extract_date(text):
    if isinstance(text, str):
        match = re.search(r'Activities\s*:\s*On Hire Information(\d{2}-\d{2}-\d{4})', text)
        if match:
            return match.group(1)
    return ''

# Apply the function to the 'On Hire Date' column
df['date'] = df['On Hire Date'].apply(extract_date)

# Save the updated DataFrame to a new Excel file
output_path = '/home/dragon/Documents/complete_seaco.xlsx'
df.to_excel(output_path, index=False)

print("Dates successfully extracted and saved to 'complete_seaco.xlsx'")
