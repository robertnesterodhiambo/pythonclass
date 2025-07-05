import os
import glob
import pandas as pd
import fitz  # PyMuPDF

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

# === Step 4: Extract 'Titular' text from first row ===
titular_value = df.loc[0, 'Titular']

# === Step 5: Open PDF with PyMuPDF ===
doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # === Step 6: Search for 'Titular:' ===
    text_instances = page.search_for("Titular:")
    
    for inst in text_instances:
        x1, y1, x2, y2 = inst  # Get bounding box
        
        print(f"'Titular:' found on page {page_num+1} at {inst}")
        
        # === Step 7: Define position to place new text ===
        # Place slightly to the right of the existing 'Titular:'
        insert_x = x2 + 5  # 5 units to the right
        insert_y = y2 - 2  # Adjust vertically to align
        
        # === Step 8: Insert the Excel value ===
        page.insert_text(
            (insert_x, insert_y),
            str(titular_value),
            fontname="helvetica-bold",  # Correct built-in font
            fontsize=11,
            color=(0, 0, 0)             # Black
        )

# === Step 9: Save edited PDF ===
output_path = "Edited_Template.pdf"
doc.save(output_path)
doc.close()

print(f"PDF updated and saved to {output_path}")
