import pandas as pd

# Step 1: Use your specific import line
df = pd.read_csv("/home/dragon/shipping_data.csv", quotechar='"', encoding='utf-8', engine='python')

# Step 2: Function to parse the `Text` column
def parse_text(text):
    if isinstance(text, str) and text.strip().lower() == "no data":
        return {
            "name": "No Data",
            "price": "No Data",
            "Estimated delivery time": "No Data",
            "Maximum weight": "No Data",
            "Dimensional weight": "No Data",
            "Maximum Size": "No Data",
            "Tracking": "No Data",
            "Frequency of departure": "No Data",
            "Insurance": "No Data"
        }

    lines = [line.strip() for line in str(text).strip().split('\n') if line.strip()]
    parsed = {
        "name": lines[0] if len(lines) > 0 else "No Data",
        "price": lines[2] if len(lines) > 2 else "No Data",
        "Estimated delivery time": "No Data",
        "Maximum weight": "No Data",
        "Dimensional weight": "No Data",
        "Maximum Size": "No Data",
        "Tracking": "Yes",  # Always Yes
        "Frequency of departure": "No Data",
        "Insurance": "No Data"
    }

    keys_map = {
        "Estimated delivery time": "Estimated delivery time",
        "Maximum weight": "Maximum weight",
        "Dimensional weight": "Dimensional weight",
        "Maximum Size": "Maximum Size",
        "Frequency of departure": "Frequency of departure",
        "Insurance": "Insurance"
    }

    for i, line in enumerate(lines):
        for key in keys_map:
            if line.startswith(key):
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines):
                    parsed[keys_map[key]] = lines[j].strip()
                break

    return parsed

# Step 3: Apply parsing
parsed_data = df["Text"].apply(parse_text)
parsed_df = pd.DataFrame(parsed_data.tolist())

# Step 4: Combine original and parsed data
result_df = pd.concat([df.drop(columns=["Text"]), parsed_df], axis=1)

# Step 5: Display and export
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(result_df.head())

result_df.to_excel("fishifast_clean.xlsx", index=False)
print("✅ Saved to fishifast_clean.xlsx")
