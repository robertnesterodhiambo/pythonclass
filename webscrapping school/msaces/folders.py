import os
import re
import shutil
from datetime import datetime
import pandas as pd
from fpdf import FPDF  # can be removed if not used

# === Step 1: Setup paths ===
source_folder = '.'
pdf_folder = 'PDF'
excel_folder = 'excel'
row_pdf_folder = 'rows_pdfs'

# === Step 2: Find latest matching Boletim_da_PI PDF by filename date ===
pdf_pattern = re.compile(r'Boletim_da_PI_-_(\d{4}-\d{2}-\d{2})\.pdf')
latest_pdf = None
latest_pdf_date = None

for filename in os.listdir(source_folder):
    match = pdf_pattern.match(filename)
    if match:
        file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
        if latest_pdf_date is None or file_date > latest_pdf_date:
            latest_pdf_date = file_date
            latest_pdf = filename

# === Step 3: Date comparison ===
today_date = datetime.today().date()

if latest_pdf_date is None:
    print("❌ No matching 'Boletim_da_PI' PDF found. Exiting.")
    exit()

if latest_pdf_date.date() != today_date:
    print(f"❌ Latest file is dated {latest_pdf_date.date()}, but today's date is {today_date}. Exiting.")
    exit()

print(f"✅ File date matches today's date: {today_date}")

# === Step 4: Proceed if dates match ===

# Create necessary folders
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(excel_folder, exist_ok=True)
os.makedirs(row_pdf_folder, exist_ok=True)

current_date_str = today_date.strftime('%Y-%m-%d')

# === Step 5: Copy PDF ===
pdf_target_path = os.path.join(pdf_folder, f"{current_date_str}.pdf")
shutil.copy2(os.path.join(source_folder, latest_pdf), pdf_target_path)
print(f"Copied PDF '{latest_pdf}' to '{pdf_target_path}'")

# === Step 6: Copy Excel ===
excel_name = 'racius_links_output.xlsx'
excel_path = os.path.join(source_folder, excel_name)

if os.path.exists(excel_path):
    excel_target_path = os.path.join(excel_folder, f"{current_date_str}.xlsx")
    shutil.copy2(excel_path, excel_target_path)
    print(f"Copied Excel '{excel_name}' to '{excel_target_path}'")

    # === Step 7: Process rows ===
    df = pd.read_excel(excel_path)

    # Step 7.1: Drop rows with any 'Not Found'
    df_cleaned = df[~df.apply(lambda row: row.astype(str).str.contains("Not Found").any(), axis=1)]

    # Step 7.2: Drop rows missing 'Morada' or 'CodigoPostal'
    df_cleaned = df_cleaned.dropna(subset=['Morada', 'CodigoPostal'])

    # Step 7.3: Save cleaned DataFrame
    cleaned_excel_path = os.path.join(excel_folder, f"{current_date_str}.xlsx")
    df_cleaned.to_excel(cleaned_excel_path, index=False)
    print(f"Saved cleaned DataFrame to '{cleaned_excel_path}'")

else:
    print("❌ Excel file 'racius_links_output.xlsx' not found.")
