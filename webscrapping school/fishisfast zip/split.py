import pandas as pd

# Load CSV
df = pd.read_csv("shipping_data.csv")

# Function to parse the `Text` field
def parse_text(text):
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    
    # Create a dictionary for the extracted fields
    parsed = {
        "name": lines[0] if len(lines) > 0 else "",
        "price": lines[2] if len(lines) > 2 else "",
        "Estimated delivery time": "",
        "Maximum weight": "",
        "Dimensional weight": "",
        "Maximum Size": "",
        "Tracking": "Yes",  # Always Yes as per instruction
        "Frequency of departure": "",
        "Insurance": ""
    }

    # Map expected headers to dictionary keys
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
            if line.strip().startswith(key):
                # Pick the next non-empty line
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
                if j < len(lines):
                    parsed[keys_map[key]] = lines[j].strip()
                break

    return parsed

# Apply the parsing to each row
parsed_data = df["Text"].apply(parse_text)
parsed_df = pd.DataFrame(parsed_data.tolist())

# Optionally, merge with original df or save/export
result_df = pd.concat([df.drop(columns=["Text"]), parsed_df], axis=1)

# Print full result
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print(result_df.head())
