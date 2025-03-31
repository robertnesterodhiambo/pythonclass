import pandas as pd
import random

# Load the CSV files
extracted_file = "extracted_unit_numbers.csv"
sea_combined_file = "sea_combined.csv"

df_extracted = pd.read_csv(extracted_file)
df_sea_combined = pd.read_csv(sea_combined_file)

# Extract Input and Unit Number values from sea_combined.csv
new_inputs = df_sea_combined["sea_combined"].tolist()
new_unit_numbers = df_sea_combined["sea_combined"].tolist()  # Same as Input

# Remove existing Input & Unit Number values in extracted_unit_numbers.csv
existing_inputs = set(df_extracted["Input"].astype(str))
filtered_inputs = [val for val in new_inputs if str(val) not in existing_inputs]

# Create a new DataFrame with the new Input and Unit Number
df_complete = pd.DataFrame({
    "Input": filtered_inputs[:len(filtered_inputs)],
    "Unit Number": filtered_inputs[:len(filtered_inputs)]  # Same as Input
})

# Randomly select values from respective columns in extracted_unit_numbers.csv
for col in df_extracted.columns[2:]:  # Skip 'Input' and 'Unit Number'
    df_complete[col] = random.choices(df_extracted[col].dropna().tolist(), k=len(df_complete))

# Take the first 5000 entries from extracted_unit_numbers.csv
df_top = df_extracted.head(5000)

# Take the remaining entries from extracted_unit_numbers.csv
df_bottom = df_extracted.iloc[5000:]

# Concatenate the data
df_final = pd.concat([df_top, df_complete, df_bottom], ignore_index=True)

# Save to CSV
output_file = "complete.csv"
df_final.to_csv(output_file, index=False)

print(f"File '{output_file}' generated successfully!")
