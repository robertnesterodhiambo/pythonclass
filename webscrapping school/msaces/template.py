import os
import glob
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter

# === Step 1: Locate Template PDF ===
pdf_path = "Template.pdf"

# === Step 2: Locate latest Excel file ===
excel_folder = "excel"
list_of_files = glob.glob(os.path.join(excel_folder, '*.xlsx'))
latest_excel = max(list_of_files, key=os.path.getmtime)
print(f"Latest Excel file found: {latest_excel}")

# === Step 3: Load Excel data ===
df = pd.read_excel(latest_excel)
print(df.head())  # View to confirm your columns

# === Step 4: Load PDF ===
reader = PdfReader(pdf_path)
writer = PdfWriter()

# === Step 5: Prepare for editing ===
# Example: For each page copy it to writer (without changes yet)
for page in reader.pages:
    writer.add_page(page)

# === Step 6: Save to a new edited PDF ===
with open("Edited_Template.pdf", "wb") as f:
    writer.write(f)

print("PDF copied to Edited_Template.pdf. Ready for incremental text edits.")
