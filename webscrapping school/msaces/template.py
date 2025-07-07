import os
import glob
import pandas as pd
import fitz  # PyMuPDF
import numpy as np

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

# === Step 4: Prepare output folder ===
output_folder = "PDF"
os.makedirs(output_folder, exist_ok=True)  # Create if doesn't exist

# === Step 5: Loop through all rows ===
for idx, row in df.iterrows():
    print(f"Processing row {idx+1} with NumeroPedido: {row['NumeroPedido']}")

    # Open fresh PDF for each row
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Helper to insert text after label
        def insert_after_label(label, value, skip_line=False, dollar_sign=False, shift_left=0, bold=True):
            if pd.isna(value):
                print(f"Skipping '{label}' insertion because value is NaN")
                return
            instances = page.search_for(label)
            for inst in instances:
                x1, y1, x2, y2 = inst
                print(f"'{label}' found on page {page_num+1} at {inst}")
                insert_x = x2 + 5 - shift_left  # apply shift left if needed
                insert_y = y2 - 2
                if skip_line:
                    insert_y = y2 + 15
                    insert_x = x1 - shift_left  # maintain shift left on skip_line too
                text_value = str(value)
                if dollar_sign:
                    text_value += " $"
                page.insert_text(
                    (insert_x, insert_y),
                    text_value,
                    fontname="helvetica" if not bold else "helvetica-bold",
                    fontsize=11,
                    color=(0, 0, 0)
                )

        # Insert fields with required formatting
        insert_after_label("Titular:", row['Titular'], shift_left=2, bold=False)
        insert_after_label("Morada:", row['Morada'], shift_left=2, bold=False)
        insert_after_label("Código Postal:", row['CodigoPostal'], shift_left=2, bold=False)
        insert_after_label("Número do pedido de Registo:", row['NumeroPedido'])
        insert_after_label("Data do Pedido de Registo:", row['DataPedido'])
        insert_after_label("Classes de Produtos/Serviços:", row['ClasseProdutos'])
        insert_after_label("Validade da Vigilância:", row['ValidadeInicio'])
        insert_after_label("Data:", row['DataDocumento'])

        # Insert Importância: beneath label, skip line, with dollar sign
        insert_after_label("Importância:", row['ValorImportancia'], skip_line=True, dollar_sign=True)

        # Insert IVA (23%): beneath label, skip line, with dollar sign
        insert_after_label("IVA (23%):", row['IVA'], skip_line=True, dollar_sign=True)

        # Insert TOTAL: beneath label, skip line, with dollar sign
        insert_after_label("TOTAL:", row['ValorTotal'], skip_line=True, dollar_sign=True)

        # === Insert Marca values centered within provided bounds ===
        coords_list = [
            (42.47, 393.80),
            (48.96, 393.80),
            (63.95, 393.80),
            (72.95, 393.80),
            (93.43, 394.80),
            (148.89, 398.30),
            (213.35, 398.30),
            (252.32, 396.30),
            (286.29, 396.30),
        ]

        # Provided bounding box for centering
        box_left = 37.97
        box_right = 297.28
        box_top = 293.35
        box_bottom = 530.23
        box_width = box_right - box_left
        box_height = box_bottom - box_top

        marca_value = row['Marca']
        if not pd.isna(marca_value):
            marca_values = str(marca_value).split(',')
            if len(marca_values) > len(coords_list):
                print(f"Warning: Too many Marca values ({len(marca_values)}), only first {len(coords_list)} will be inserted.")

            for i, (x, y) in enumerate(coords_list):
                if i < len(marca_values):
                    text_value = marca_values[i].strip()
                    font_size = 16
                    font_name = "Times-Roman"

                    # Calculate text width for horizontal centering
                    text_width = fitz.get_text_length(text_value, fontname=font_name, fontsize=font_size)
                    centered_x = box_left + (box_width - text_width) / 2

                    # Calculate vertical center and adjust for baseline
                    centered_y = box_top + (box_height / 2) + (font_size / 2.8)

                    page.insert_text(
                        (centered_x, centered_y),
                        text_value,
                        fontname=font_name,
                        fontsize=font_size,
                        color=(0, 0, 0)
                    )
                    print(f"Inserted Marca value '{text_value}' at centered ({centered_x}, {centered_y}) within box")
        else:
            print("Marca is missing or NaN; skipping Marca insertion.")

    # Save PDF with NumeroPedido filename in PDF folder
    output_path = os.path.join(output_folder, f"{row['NumeroPedido']}.pdf")
    doc.save(output_path)
    doc.close()

    print(f"Saved PDF: {output_path}")

print("All rows processed.")
