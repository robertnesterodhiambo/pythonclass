import pandas as pd
import numpy as np
import random

# === File paths ===
CSV_PATH = "/home/dragon/GIT/pythonclass/webscrapping school/plannetexpress/shipping_results.csv"
XLSX_PATH = "1stackry.xlsx"  # This will be created/overwritten in the same directory

# === Load CSV ===
df_csv = pd.read_csv(CSV_PATH)

# === Select 15,000 rows ===
df_15k = df_csv.head(15000)

# === Map to 1stackry.xlsx columns ===
column_map = {
    "To Country":         "Recieving Country",
    "To City":            "Recieving City",
    "Postal Code":        "Recieving Zipcode",
    "Weight (lbs)":       "Weight in (LBS)",
    "Shipping Method":    "Shipping Method",
    "Estimated Delivery": "Estimated Delivery Time",
    "Price":              "Price in USD",
}

# === Rename and order columns ===
df_mapped = (
    df_15k
    .rename(columns=column_map)
    [list(column_map.values())]
    .assign(**{"SHIPPING METHODS": df_15k["Shipping Method"].values})
)

# === Clean data to avoid "Not valid input" errors ===

# 1. Replace NaN, inf values with empty strings
df_clean = df_mapped.replace([np.nan, np.inf, -np.inf], '')

# 2. Convert columns to appropriate data types (numeric where applicable)
df_clean["Weight in (LBS)"] = pd.to_numeric(df_clean["Weight in (LBS)"], errors='coerce')  # Force numbers in Weight column

# 3. Strip leading/trailing spaces from all string columns
df_clean = df_clean.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# 4. Remove non-UTF8 characters
df_clean = df_clean.applymap(lambda x: x.encode('utf-8', 'ignore').decode('utf-8') if isinstance(x, str) else x)

# 5. Handle Excel formulas like strings (e.g., =SUM(...) in cells)
df_clean = df_clean.applymap(lambda x: f"'{x}" if isinstance(x, str) and x.startswith('=') else x)

# === Adjust Price and Estimated Delivery Time ===

# Function to adjust price by ±10% or leave it same
def adjust_price(price_str):
    if pd.isna(price_str):
        return price_str
    try:
        # Remove the ' USD' part, convert to float, and adjust
        price = float(price_str.replace(' USD', ''))
        adjustment_factor = random.choice([1.1, 0.9, 1])  # +10%, -10%, or no change
        adjusted_price = round(price * adjustment_factor, 2)  # Round to 2 decimal places
        return f"{adjusted_price} USD"
    except ValueError:
        return price_str  # Return the original if there's an error

# Function to adjust Estimated Delivery Time by adding ±10% or leaving it same
def adjust_delivery_time(time_str):
    if isinstance(time_str, str):
        # Extract numeric ranges from the string (e.g., "8-12 business days")
        try:
            parts = time_str.split(' ')[0].split('-')
            min_days = int(parts[0])
            max_days = int(parts[1])
            adjustment_factor = random.choice([1.1, 0.9, 1])  # +10%, -10%, or no change
            
            # Apply adjustment
            min_days_adjusted = round(min_days * adjustment_factor)
            max_days_adjusted = round(max_days * adjustment_factor)
            
            return f"{min_days_adjusted}-{max_days_adjusted} business days"
        except ValueError:
            return time_str  # Return original if format is unexpected
    return time_str  # Return original if not a string

# Apply adjustments
df_clean["Price in USD"] = df_clean["Price in USD"].apply(adjust_price)
df_clean["Estimated Delivery Time"] = df_clean["Estimated Delivery Time"].apply(adjust_delivery_time)

# === Write to Excel ===
df_clean.to_excel(XLSX_PATH, index=False)

print(f"✅ 15,000 adjusted entries written to {XLSX_PATH}")
