import mysql.connector
import pandas as pd
import re

# Connect to MySQL
conn = mysql.connector.connect(
    host='104.238.220.190',
    user='cashprohomebuyer_new_real_state',
    password='KH8lhGoLK4Sl',
    database='cashprohomebuyer_new_real_state'
)

# Load data
df = pd.read_sql("SELECT * FROM GaPub", conn)
conn.close()

# Smart suspicious word check
def is_suspicious(text):
    if not text:
        return True
    suspicious_words = ['notice', 'court', 'order', 'legal', 'estate']
    clean = text.lower().strip()
    return clean in suspicious_words or all(word in clean for word in suspicious_words)

# Address patterns
address_patterns = [
    r'(\d{1,6}[\w\s.#\-]*?),\s*([A-Za-z\s]+?),\s*GA\s+(\d{5})',
    r'(\d{1,6}[\w\s.#\-]+?)\s+([A-Za-z\s]+?)\s+GA\s+(\d{5})',
    r'(\d{1,6}[\w\s.#\-]*?),\s*([A-Za-z\s]+?),\s*GA\b',
    r'(\d{1,6}[\w\s.#\-]+?)\s+([A-Za-z\s]+?)\s+GA\b',
    r'(\d{1,6}[\w\s.#\-]+?)\s+GA\s+(\d{5})',
    r'([A-Za-z\s]+?),\s*GA\s+(\d{5})',
    r'([\d]{1,6}[\w\s.#\-&,]*?),\s*([A-Za-z\s]+?),\s*GA\s+(\d{5})',
    r'([\d]{1,6}[\w\s.#\-&,]+)\s+([A-Za-z\s]+)\s+GA\s+(\d{5})',
    r'([\d]{1,6}[\w\s.#\-&,]+)\s+GA\s+(\d{5})',
    r'([A-Za-z\s]+),?\s+GA\s+(\d{5})',
    r'GA\s+(\d{5})',
    r'([\d]{1,6}[\w\s.#\-&,]*?),\s*([A-Za-z\s]+?),\s*Georgia\s+(\d{5})',
    r'Suite\s*\d+\s*(?:at\s*)?(?:[\w\s]+?),\s*([\d]{1,6}[\w\s.#\-&,]+),\s*([A-Za-z\s]+),\s*(?:GA|Georgia)\s+(\d{5})',
    r'at\s+([\d]{1,6}[\w\s.#\-&,]+),\s*([A-Za-z\s]+),\s*(?:GA|Georgia)\s+(\d{5})'
]

# Function to clean leading junk and extract address
def extract_address(text):
    if pd.isna(text):
        return pd.Series([None, None, None])

    for pattern in address_patterns:
        regex = re.compile(pattern, re.IGNORECASE)
        matches = list(regex.finditer(text))
        if matches:
            for match in reversed(matches):  # try from last to first
                groups = match.groups()
                street = city = zip_code = None
                if len(groups) == 3:
                    street, city, zip_code = groups
                elif len(groups) == 2:
                    if re.search(r'\d', groups[0]):
                        street = groups[0]
                        zip_code = groups[1]
                    else:
                        city = groups[0]
                        zip_code = groups[1]
                elif len(groups) == 1:
                    zip_code = groups[0]

                # Clean up
                if street:
                    street = street.strip()
                    # Remove junk before house number
                    street = re.sub(r'^.*?(?=\d{1,6})', '', street).strip()
                if city:
                    city = city.strip()
                if zip_code:
                    zip_code = zip_code.strip()

                # Check if suspicious
                if not is_suspicious(street) and not is_suspicious(city):
                    return pd.Series([street, city, zip_code])
    return pd.Series([None, None, None])

# Clean GA+punctuation
def clean_notice(text):
    if pd.isna(text):
        return text
    return re.sub(r'\bGA[.,;]?', 'GA ', text, flags=re.IGNORECASE)

# Apply cleaning
df['Clean_Notice'] = df['Notice'].apply(clean_notice)

# Extract addresses
df[['Extracted_Street', 'Extracted_City', 'Extracted_Zip_Code']] = df['Clean_Notice'].apply(extract_address)

# Optional: show which match worked (for debugging)
df['Matched_Text'] = df['Clean_Notice'].apply(
    lambda x: next((m.group(0) for p in address_patterns for m in re.finditer(p, str(x), re.IGNORECASE)), None)
)

# Display
print(df[['Notice', 'Extracted_Street', 'Extracted_City', 'Extracted_Zip_Code', 'Matched_Text']].head(15))
