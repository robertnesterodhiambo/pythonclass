import os
import glob
import pandas as pd

EXCEL_DIR = "excel"
DB_FILE = "DB_excel.xlsx"

# === Step 1: Find the latest Excel file ===
def find_latest_excel_file(folder):
    files = glob.glob(os.path.join(folder, '*.xlsx'))
    if not files:
        raise FileNotFoundError("No Excel files found in the folder.")
    latest_file = max(files, key=os.path.getmtime)
    return latest_file

# === Step 2: Load existing DB_excel.xlsx ===
def load_existing_db():
    if os.path.exists(DB_FILE):
        return pd.read_excel(DB_FILE)
    else:
        return pd.DataFrame()

# === Step 3: Append new data if not duplicate ===
def append_unique_rows(db_df, new_df):
    combined_df = pd.concat([db_df, new_df], ignore_index=True)
    combined_df = combined_df.drop_duplicates()
    new_rows_count = len(combined_df) - len(db_df)
    duplicate_count = len(new_df) - new_rows_count
    return combined_df, duplicate_count

# === Main Logic ===
def main():
    latest_file = find_latest_excel_file(EXCEL_DIR)
    print(f"Latest file: {latest_file}")

    new_data = pd.read_excel(latest_file)
    db_data = load_existing_db()

    updated_db, duplicate_count = append_unique_rows(db_data, new_data)

    updated_db.to_excel(DB_FILE, index=False)
    
    print(f"✅ DB updated. {len(updated_db)} total rows.")
    if duplicate_count > 0:
        print(f"⚠️ {duplicate_count} duplicate rows were skipped.")
    else:
        print("✅ No duplicates found. All rows added.")

if __name__ == "__main__":
    main()