import pandas as pd

# Load the data
df = pd.read_csv('collected_data.csv')

# Function to extract the third line after "User name edited by"
def extract_third_line(text):
    # Split the text by lines
    lines = text.splitlines()
    
    # Find the line that contains "User name edited by"
    for i, line in enumerate(lines):
        if "User name edited by" in line:
            # Check if there are at least three lines following this line
            if i + 3 < len(lines):
                return lines[i + 3]  # Return the third line after "User name edited by"
            else:
                return ""  # Return an empty string if not enough lines after
    return ""  # Return an empty string if "User name edited by" is not found

# Apply the function to the 'Text' column and store the result in a new column called 'old_name'
df['old_name'] = df['Text'].apply(extract_third_line)

# Display the modified DataFrame
print(df)
