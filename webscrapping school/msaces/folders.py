import os
import re
import shutil
from datetime import datetime

# Define the source folder
source_folder = '.'  # current directory

# Define target folders
pdf_folder = 'PDF'
excel_folder = 'excel'

# Create folders if not exist
os.makedirs(pdf_folder, exist_ok=True)
os.makedirs(excel_folder, exist_ok=True)

# Get today's date string
current_date_str = datetime.today().strftime('%Y-%m-%d')

# ----- 1. Handle PDF -----
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

# ----- 2. Handle Excel -----
excel_name = 'racius_links_output.xlsx'
if os.path.exists(os.path.join(source_folder, excel_name)):
    excel_target_path = os.path.join(excel_folder, f"{current_date_str}.xlsx")
    shutil.copy2(os.path.join(source_folder, excel_name), excel_target_path)
    print(f"Copied Excel '{excel_name}' to '{excel_target_path}'")
else:
    print("Excel file 'racius_links_output.xlsx' not found.")
