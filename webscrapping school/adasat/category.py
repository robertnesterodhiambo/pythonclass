import pandas as pd
import numpy as np

# Load the Excel file into a DataFrame
df = pd.read_excel('clean collection.xlsx')

# Define a function to split 'Product Category' and handle cases where the value is not a string
def split_category(category):
    if isinstance(category, str):
        parts = category.split('- ')
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        else:
            return parts[0].strip(), None
    else:
        return None, None

# Apply the function to split 'Product Category' into 'Category' and 'Subcategory'
df['Category'], df['Subcategory'] = zip(*df['Product Category'].apply(split_category))

# Drop the original 'Product Category' column
df = df.drop(columns=['Product Category'])

# Save the updated DataFrame to a new Excel file
df.to_excel('cleaned_collection.xlsx', index=False)

# Display the first 5 rows of the updated DataFrame
print(df.head(5))
