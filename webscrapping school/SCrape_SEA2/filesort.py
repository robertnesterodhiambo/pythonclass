import pandas as pd

# Load the Excel file
file_path = "SEA.xlsx"  # Ensure this file is in the same folder as your script
df = pd.read_excel(file_path)

# Stack all columns beneath each other, keeping NaN values initially
df_stacked = df.melt(value_name="sea_combined")[["sea_combined"]]

# Drop NaN values after stacking
df_stacked = df_stacked.dropna()

# Save to CSV
df_stacked.to_csv("sea_combined.csv", index=False)

print("Stacked data saved as 'sea_combined.csv'.")
