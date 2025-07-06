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
        def insert_after_label(label, value, skip_line=False, dollar_sign=False):
            instances = page.search_for(label)
            for inst in instances:
                x1, y1, x2, y2 = inst
                print(f"'{label}' found on page {page_num+1} at {inst}")
                insert_x = x2 + 5
                insert_y = y2 - 2
                if skip_line:
                    insert_y = y2 + 15
                    insert_x = x1  # left aligned with label
                text_value = str(value)
                if dollar_sign:
                    text_value += " $"
                page.insert_text(
                    (insert_x, insert_y),
                    text_value,
                    fontname="helvetica-bold",
                    fontsize=11,
                    color=(0, 0, 0)
                )

        # Insert fields without skip line or dollar sign
        insert_after_label("Titular:", row['Titular'])
        insert_after_label("Morada:", row['Morada'])
        insert_after_label("Código Postal:", row['CodigoPostal'])
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

    # Save PDF with NumeroPedido filename in PDF folder
    output_path = os.path.join(output_folder, f"{row['NumeroPedido']}.pdf")
    doc.save(output_path)
    doc.close()

    print(f"Saved PDF: {output_path}")

print("All rows processed.")
