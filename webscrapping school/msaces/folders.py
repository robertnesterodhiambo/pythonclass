import os
import re
import shutil
from datetime import datetime
import pandas as pd
from fpdf import FPDF

# === Step 1: Setup paths ===
source_folder = '.'
pdf_folder = 'PDF'
excel_folder = 'excel'
row_pdf_folder = 'rows_pdfs'

# Create necessary folders
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(excel_folder, exist_ok=True)
os.makedirs(row_pdf_folder, exist_ok=True)

# Get today's date string
current_date_str = datetime.today().strftime('%Y-%m-%d')

# === Step 2: Copy latest Boletim_da_PI PDF ===
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

if latest_pdf:
    pdf_target_path = os.path.join(pdf_folder, f"{current_date_str}.pdf")
    shutil.copy2(os.path.join(source_folder, latest_pdf), pdf_target_path)
    print(f"Copied PDF '{latest_pdf}' to '{pdf_target_path}'")
else:
    print("No matching PDF found.")

# === Step 3: Copy racius_links_output.xlsx ===
excel_name = 'racius_links_output.xlsx'
excel_path = os.path.join(source_folder, excel_name)

if os.path.exists(excel_path):
    excel_target_path = os.path.join(excel_folder, f"{current_date_str}.xlsx")
    shutil.copy2(excel_path, excel_target_path)
    print(f"Copied Excel '{excel_name}' to '{excel_target_path}'")

    # === Step 4: Process rows and generate per-row PDFs ===
    df = pd.read_excel(excel_path)

    # Drop rows with any 'Not Found' in any cell
    df_cleaned = df[~df.apply(lambda row: row.astype(str).str.contains("Not Found").any(), axis=1)]

    # Generate PDF from each row
    for _, row in df_cleaned.iterrows():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for col in df.columns:
            value = str(row[col])
            pdf.multi_cell(0, 10, f"{col}: {value}", border=0)

        numero_pedido = str(row['NumeroPedido'])
        row_pdf_path = os.path.join(row_pdf_folder, f"{numero_pedido}.pdf")
        pdf.output(row_pdf_path)

    print(f"Generated {len(df_cleaned)} row PDFs in '{row_pdf_folder}'")

else:
    print("Excel file 'racius_links_output.xlsx' not found.")
