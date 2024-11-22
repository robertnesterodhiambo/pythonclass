import pandas as pd
import re

# Load the CSV file
csv_file_path = "merged_output.csv"
data = pd.read_csv(csv_file_path)

# Function to extract text after "ThankReport" following "User name edited by"
def extract_time(cell_text):
    if "User name edited by" in cell_text:
        match = re.search(r"ThankReport(.*)", cell_text)
        if match:
            return match.group(1).strip()
    return None

# Apply the function to the 'text' column and create a new column 'time'
data['time'] = data['Text'].dropna().apply(extract_time)

# Save the updated DataFrame to a new CSV file
output_file_path = "updated_output.csv"
data.to_csv(output_file_path, index=False)

print(f"DataFrame saved to {output_file_path}")
