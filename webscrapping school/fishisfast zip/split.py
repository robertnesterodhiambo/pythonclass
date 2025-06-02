import pandas as pd
import numpy as np

file_path = '/home/dragon/DATA/shipping_data.csv'
output_path = '/home/dragon/DATA/shipping_data_cleaned.xlsx'

# Read the CSV
df = pd.read_csv(
    file_path,
    delimiter=",",
    quotechar='"',
    on_bad_lines='skip',
    engine='python'
)

# Function to extract structured shipping data
def extract_shipping_data(text):
    if not isinstance(text, str) or "Estimated delivery time" not in text:
        return {
            "Shipping Method": "No Data",
            "Price": "No Data",
            "Estimated Delivery Time": "No Data",
            "Maximum Weight": "No Data",
            "Dimensional Weight": "No Data",
            "Maximum Size": "No Data",
            "Tracking": "No Data",
            "Frequency of Departure": "No Data",
            "Insurance": "No Data"
        }

    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    def extract_after(label):
        for i, line in enumerate(lines):
            if line.lower().startswith(label.lower()):
                return lines[i + 1] if i + 1 < len(lines) else "No Data"
        return "No Data"

    return {
        "Shipping Method": lines[0] if len(lines) > 0 else "No Data",
        "Price": lines[2] if len(lines) > 2 else "No Data",
        "Estimated Delivery Time": extract_after("Estimated delivery time"),
        "Maximum Weight": extract_after("Maximum weight"),
        "Dimensional Weight": extract_after("Dimensional weight"),
        "Maximum Size": extract_after("Maximum Size"),
        "Tracking": "Yes",  # Marked as "Yes" by default
        "Frequency of Departure": extract_after("Frequency of departure"),
        "Insurance": extract_after("Insurance")
    }

# Apply extraction to each row
shipping_details = df['Text'].apply(extract_shipping_data).apply(pd.Series)

# Merge extracted columns into original DataFrame
df = pd.concat([df.drop(columns=["Text"]), shipping_details], axis=1)

# Show result
print(df.head())
df.to_excel(output_path, index=False)

print(f"Saved cleaned shipping data to {output_path}")