import pandas as pd

# Set pandas display options to show all rows and columns
    # Auto-adjust width
pd.set_option('display.max_colwidth', None) # Display full content in each column

# Load the data from both CSV files
df1 = pd.read_csv('collected_data.csv')     # Main DataFrame with 'Text' and 'Link' columns
df2 = pd.read_csv('output_updated.csv')     # Secondary DataFrame with 'edit_link' column

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

# Apply the function to the 'Text' column in df1 and create a new column 'old_name'
df1['old_name'] = df1['Text'].apply(extract_third_line)

# Perform an inner join on 'Link' and 'edit_link' columns
merged_df = pd.merge(df1, df2, left_on='Link', right_on='edit_link', how='inner')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_output.csv', index=False)

# Display confirmation message
print("Merged DataFrame saved to 'merged_output.csv'")
