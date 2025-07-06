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

# === Step 4: Extract values from first row ===
titular_value = df.loc[0, 'Titular']
morada_value = df.loc[0, 'Morada']
codigo_postal_value = df.loc[0, 'CodigoPostal']
numero_pedido_value = df.loc[0, 'NumeroPedido']
data_pedido_value = df.loc[0, 'DataPedido']
classe_produtos_value = df.loc[0, 'ClasseProdutos']
validade_inicio_value = df.loc[0, 'ValidadeInicio']
data_documento_value = df.loc[0, 'DataDocumento']
valor_importancia_value = df.loc[0, 'ValorImportancia']
iva_value = df.loc[0, 'IVA']

# === Step 5: Open PDF with PyMuPDF ===
doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # === Insert Titular ===
    titular_instances = page.search_for("Titular:")
    for inst in titular_instances:
        x1, y1, x2, y2 = inst
        print(f"'Titular:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(titular_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Morada ===
    morada_instances = page.search_for("Morada:")
    for inst in morada_instances:
        x1, y1, x2, y2 = inst
        print(f"'Morada:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(morada_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Código Postal ===
    codigo_postal_instances = page.search_for("Código Postal:")
    for inst in codigo_postal_instances:
        x1, y1, x2, y2 = inst
        print(f"'Código Postal:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(codigo_postal_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Número do pedido de Registo ===
    numero_pedido_instances = page.search_for("Número do pedido de Registo:")
    for inst in numero_pedido_instances:
        x1, y1, x2, y2 = inst
        print(f"'Número do pedido de Registo:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(numero_pedido_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Data do Pedido de Registo ===
    data_pedido_instances = page.search_for("Data do Pedido de Registo:")
    for inst in data_pedido_instances:
        x1, y1, x2, y2 = inst
        print(f"'Data do Pedido de Registo:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(data_pedido_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Classes de Produtos/Serviços ===
    classe_produtos_instances = page.search_for("Classes de Produtos/Serviços:")
    for inst in classe_produtos_instances:
        x1, y1, x2, y2 = inst
        print(f"'Classes de Produtos/Serviços:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(classe_produtos_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )

    # === Insert Validade da Vigilância ===
    validade_vigilancia_instances = page.search_for("Validade da Vigilância:")
    for inst in validade_vigilancia_instances:
        x1, y1, x2, y2 = inst
        print(f"'Validade da Vigilância:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(validade_inicio_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
        
    # === Insert Data: ===
    data_instances = page.search_for("Data:")
    for inst in data_instances:
        x1, y1, x2, y2 = inst
        print(f"'Data:' found on page {page_num+1} at {inst}")
        insert_x = x2 + 5
        insert_y = y2 - 2
        page.insert_text(
            (insert_x, insert_y),
            str(data_documento_value),
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
    
    # === Insert Importância: (beneath with € sign, with extra space) ===
    importancia_instances = page.search_for("Importância:")
    for inst in importancia_instances:
        x1, y1, x2, y2 = inst
        print(f"'Importância:' found on page {page_num+1} at {inst}")
        insert_x = x1  # left aligned with label
        insert_y = y2 + 15  # bigger vertical gap to skip one line
        
        valor_importancia_text = str(valor_importancia_value) + " $"
        
        page.insert_text(
            (insert_x, insert_y),
            valor_importancia_text,
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )
        
    # === Insert IVA (23%): (beneath, skip line, with $ sign) ===
    iva_instances = page.search_for("IVA (23%):")
    for inst in iva_instances:
        x1, y1, x2, y2 = inst
        print(f"'IVA (23%):' found on page {page_num+1} at {inst}")
        insert_x = x1  # left aligned with label
        insert_y = y2 + 15  # move down to skip one line
        
        iva_text = str(iva_value) + " $"
        
        page.insert_text(
            (insert_x, insert_y),
            iva_text,
            fontname="helvetica-bold",
            fontsize=11,
            color=(0, 0, 0)
        )

# === Step 6: Save edited PDF ===
output_path = "Edited_Template.pdf"
doc.save(output_path)
doc.close()

print(f"PDF updated and saved to {output_path}")
