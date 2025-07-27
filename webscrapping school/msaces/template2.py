import os
import glob
import pandas as pd
import fitz  # PyMuPDF
import numpy as np
import unicodedata
from PIL import Image  # Added for image size calculations

# -- coding: utf-8 --

# === Step 1: Locate Template PDF === 
pdf_path = "Template2.pdf"

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

# === Helper function to wrap text to width ===
def wrap_text_to_width(text, fontname, fontsize, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        test_width = fitz.get_text_length(test_line, fontname=fontname, fontsize=fontsize)
        if test_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

# === Step 5: Loop through all rows ===
for idx, row in df.iterrows():
    marca_value = row['Marca']
    # === Only proceed if Marca is missing or empty ===
    if pd.notna(marca_value) and any(mv.strip() for mv in str(marca_value).split(',')):
        print(f"Skipping row {idx+1} with NumeroPedido {row['NumeroPedido']} because Marca is NOT empty")
        continue

    print(f"Processing row {idx+1} with NumeroPedido: {row['NumeroPedido']} (Marca is empty)")

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        border_thickness = 20

        # White out the borders
        page.draw_rect(fitz.Rect(0, 0, page.rect.width, border_thickness), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
        page.draw_rect(fitz.Rect(0, page.rect.height - border_thickness, page.rect.width, page.rect.height), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
        page.draw_rect(fitz.Rect(0, 0, border_thickness, page.rect.height), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)
        page.draw_rect(fitz.Rect(page.rect.width - border_thickness, 0, page.rect.width, page.rect.height), color=(1, 1, 1), fill=(1, 1, 1), overlay=True)

        def insert_after_label(label, value, skip_line=False, dollar_sign=False, shift_left=0, bold=True, leading_spaces=0):
            if pd.isna(value):
                print(f"Skipping '{label}' insertion because value is NaN")
                return
            instances = page.search_for(label)
            for inst in instances:
                x1, y1, x2, y2 = inst
                insert_x = x2 + 5 - shift_left
                insert_y = y2 - 2
                if skip_line:
                    insert_y = y2 + 15
                    insert_x = x1 - shift_left

                if isinstance(value, float) and value.is_integer():
                    text_value = str(int(value))
                else:
                    text_value = str(value)

                text_value = (" " * leading_spaces) + text_value
                font_name = "helvetica" if label == "Código Postal:" else ("Times-Roman" if not bold else "Times-Bold")

                page.insert_text(
                    (insert_x, insert_y),
                    text_value,
                    fontname=font_name,
                    fontsize=11,
                    color=(0, 0, 0)
                )

        def insert_wrapped(label, value, shift_left=2, max_line_length=40, font_size=11, bold=False, leading_spaces=0):
            if pd.isna(value):
                print(f"Skipping '{label}' insertion because value is NaN")
                return
            instances = page.search_for(label)
            for inst in instances:
                x1, y1, x2, y2 = inst

                text_value = str(value)
                words = text_value.split()
                lines = []
                current_line = ""

                for word in words:
                    if len(current_line + " " + word) <= max_line_length if current_line else len(word) <= max_line_length:
                        if current_line:
                            current_line += " " + word
                        else:
                            current_line = word
                    else:
                        lines.append(current_line)
                        current_line = word
                        if len(lines) == 2:
                            break

                if current_line and len(lines) < 2:
                    lines.append(current_line)

                if len(lines) == 1:
                    lines.append("")

                len_first = len(lines[0])
                len_second = len(lines[1])
                if len_second < len_first:
                    padding = " " * (len_first - len_second)
                    lines[1] += padding

                font_name = "helvetica-bold" if bold else "helvetica"
                insert_x = x2 + 5 - shift_left
                insert_y = y2 - 2
                space_prefix = " " * leading_spaces

                for i, line in enumerate(lines):
                    page.insert_text(
                        (insert_x, insert_y + i * (font_size + 4)),
                        space_prefix + line,
                        fontname=font_name,
                        fontsize=font_size,
                        color=(0, 0, 0)
                    )

        # === Insert fields ===
        insert_wrapped("Titular:", row['Titular'], shift_left=2, bold=False, leading_spaces=3)
        insert_wrapped("Morada:", row['Morada'], shift_left=2, bold=False, leading_spaces=3)
        insert_after_label("Código Postal:", row['CodigoPostal'], shift_left=2, bold=False, leading_spaces=3)

        insert_after_label("Número do pedido de Registo:", row['NumeroPedido'],  skip_line=True, bold=True)
        insert_after_label("Data do Pedido de Registo:", row['DataPedido'], skip_line=True, bold=True)

        validade_inicio = row['ValidadeInicio']
        validade_fim = row['ValidadeFim']
        if pd.notna(validade_inicio) and pd.notna(validade_fim):
            validade_text = f"De {validade_inicio} até {validade_fim}"
            insert_after_label("Validade da Vigilância:", validade_text, skip_line=True, bold=True)
        else:
            print(f"Skipping Validade da Vigilância insertion because ValidadeInicio or ValidadeFim is missing for NumeroPedido {row['NumeroPedido']}")

        insert_after_label("Classes de Produtos/Serviços:", row['ClasseProdutos'],  skip_line=True, bold=True)
        insert_after_label("Data:", row['DataDocumento'], skip_line=True, bold=True)

        # === Insert centered image ===
        image_filename = f"{row['NumeroPedido']}.jpeg"
        image_path = os.path.join("extracted_image", image_filename)

        if os.path.exists(image_path):
            image_rect = fitz.Rect(36.97, 294.35, 298.78, 531.23)
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
                    rect_width = image_rect.width
                    rect_height = image_rect.height

                    scale = min(rect_width / img_width, rect_height / img_height)
                    new_width = img_width * scale
                    new_height = img_height * scale

                    x0 = image_rect.x0 + (rect_width - new_width) / 2
                    y0 = image_rect.y0 + (rect_height - new_height) / 2
                    x1 = x0 + new_width
                    y1 = y0 + new_height

                    doc[page_num].insert_image(fitz.Rect(x0, y0, x1, y1), filename=image_path)
                    print(f"Inserted centered image for NumeroPedido {row['NumeroPedido']}")
            except Exception as e:
                print(f"Failed to insert image for NumeroPedido {row['NumeroPedido']}: {e}")
        else:
            print(f"Image not found for NumeroPedido {row['NumeroPedido']} at {image_path}")

    output_path = os.path.join(output_folder, f"{row['NumeroPedido']}.pdf")
    doc.save(output_path)
    doc.close()

    print(f"Saved PDF: {output_path}")

print("All rows processed.")
