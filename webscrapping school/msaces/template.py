import os
import glob
import pandas as pd
import fitz  # PyMuPDF
import numpy as np
import unicodedata

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
    if pd.isna(marca_value) or not any(mv.strip() for mv in str(marca_value).split(',')):
        print(f"Skipping row {idx+1} with NumeroPedido {row['NumeroPedido']} because Marca is missing or empty")
        continue

    print(f"Processing row {idx+1} with NumeroPedido: {row['NumeroPedido']}")

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # === Overlay white rectangles on all sides to cover black borders ===
        border_thickness = 20  # adjust as needed

        # Top
        page.draw_rect(
            fitz.Rect(0, 0, page.rect.width, border_thickness),
            color=(1, 1, 1),
            fill=(1, 1, 1),
            overlay=True
        )
        # Bottom
        page.draw_rect(
            fitz.Rect(0, page.rect.height - border_thickness, page.rect.width, page.rect.height),
            color=(1, 1, 1),
            fill=(1, 1, 1),
            overlay=True
        )
        # Left
        page.draw_rect(
            fitz.Rect(0, 0, border_thickness, page.rect.height),
            color=(1, 1, 1),
            fill=(1, 1, 1),
            overlay=True
        )
        # Right
        page.draw_rect(
            fitz.Rect(page.rect.width - border_thickness, 0, page.rect.width, page.rect.height),
            color=(1, 1, 1),
            fill=(1, 1, 1),
            overlay=True
        )

        def insert_after_label(label, value, skip_line=False, dollar_sign=False, shift_left=0, bold=True, leading_spaces=0):
            if pd.isna(value):
                print(f"Skipping '{label}' insertion because value is NaN")
                return
            instances = page.search_for(label)
            for inst in instances:
                x1, y1, x2, y2 = inst
                print(f"'{label}' found on page {page_num+1} at {inst}")
                insert_x = x2 + 5 - shift_left
                insert_y = y2 - 2
                if skip_line:
                    insert_y = y2 + 15
                    insert_x = x1 - shift_left

                # Convert float ending with .0 to int
                if isinstance(value, float) and value.is_integer():
                    text_value = str(int(value))
                else:
                    text_value = str(value)

                # === Omit typing of EUR sign ===
                # if dollar_sign:
                #     euro_sign = unicodedata.lookup("EURO SIGN")
                #     text_value += f" {euro_sign}"

                text_value = (" " * leading_spaces) + text_value

                # === Make Código Postal Helvetica ===
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
                print(f"'{label}' found on page {page_num+1} at {inst}")

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

        # === Insert 11683 beneath Entidade ===
        # entidade_instances = page.search_for("Entidade")
        # for inst in entidade_instances:
        #     x1, y1, x2, y2 = inst
        #     insert_x = x1  # aligned with Entidade
        #     insert_y = y2 + 15  # beneath Entidade with spacing
        #     page.insert_text(
        #         (insert_x, insert_y),
        #         "11683",
        #         fontname="Times-Bold",
        #         fontsize=11,
        #         color=(0, 0, 0)
        #         )
        #     print(f"Inserted '11683' beneath Entidade at ({insert_x}, {insert_y})")
            
        # === Insert 367098190 beneath Referência ===
        # referencia_instances = page.search_for("Referência")
        # for inst in referencia_instances:
        #     x1, y1, x2, y2 = inst
        #     insert_x = x1  # aligned with Referência
        #     insert_y = y2 + 15  # beneath Referência with spacing
        #     page.insert_text(
        #         (insert_x, insert_y),
        #         "367098190",
        #         fontname="Times-Bold",
        #         fontsize=11,
        #         color=(0, 0, 0)
        #         )
        #     print(f"Inserted '367098190' beneath Referência at ({insert_x}, {insert_y})")


        # === Insert 34,44€ beneath Montante ===
        # montante_instances = page.search_for("Montante")
        # for inst in montante_instances:
        #     x1, y1, x2, y2 = inst
        #     insert_x = x1  # aligned with Montante
        #     insert_y = y2 + 15  # beneath Montante with spacing
        #     page.insert_text(
        #         (insert_x, insert_y),
        #         "34,44€",
        #         fontname="Times-Bold",
        #         fontsize=11,
        #         color=(0, 0, 0)
        #         )
        #     print(f"Inserted '34,44€' beneath Montante at ({insert_x}, {insert_y})")


        # === Insert wrapped Titular ===
        insert_wrapped("Titular:", row['Titular'], shift_left=2, bold=False, leading_spaces=3)

        # === Insert wrapped Morada ===
        insert_wrapped("Morada:", row['Morada'], shift_left=2, bold=False, leading_spaces=3)

        # === Insert Código Postal with leading spaces ===
        insert_after_label("Código Postal:", row['CodigoPostal'], shift_left=2, bold=False, leading_spaces=3)

        insert_after_label("Número do pedido de Registo:", row['NumeroPedido'],  skip_line=True, bold=True)
        insert_after_label("Data do Pedido de Registo:", row['DataPedido'], skip_line=True, bold=True)

        # === Insert Validade da Vigilância with ValidadeInicio and ValidadeFim combined ===
        validade_inicio = row['ValidadeInicio']
        validade_fim = row['ValidadeFim']

        if pd.notna(validade_inicio) and pd.notna(validade_fim):
            validade_text = f"De {validade_inicio} até {validade_fim}"
            insert_after_label("Validade da Vigilância:", validade_text, skip_line=True, bold=True)
        else:
            print(f"Skipping Validade da Vigilância insertion because ValidadeInicio or ValidadeFim is missing for NumeroPedido {row['NumeroPedido']}")

        insert_after_label("Classes de Produtos/Serviços:", row['ClasseProdutos'],  skip_line=True, bold=True)
        insert_after_label("Data:", row['DataDocumento'], skip_line=True, bold=True)

        # === Omit typing into Importância, IVA (23%), TOTAL ===
        # insert_after_label("Importância:", row['ValorImportancia'], skip_line=True, dollar_sign=True)
        # insert_after_label("IVA (23%):", row['IVA'], skip_line=True, dollar_sign=True)
        # insert_after_label("TOTAL:", row['ValorTotal'], skip_line=True, dollar_sign=True)

        coords_list = [
            (42.47, 393.80), (48.96, 393.80), (63.95, 393.80),
            (72.95, 393.80), (93.43, 394.80), (148.89, 398.30),
            (213.35, 398.30), (252.32, 396.30), (286.29, 396.30),
        ]

        box_left = 36.97
        box_right = 297.28
        box_top = 293.35
        box_bottom = 530.23
        box_width = box_right - box_left
        box_height = box_bottom - box_top

        marca_values = [mv.strip() for mv in str(marca_value).split(',') if mv.strip()]

        if len(marca_values) > len(coords_list):
            print(f"Warning: Too many Marca values ({len(marca_values)}), only first {len(coords_list)} will be inserted.")

        for i, (x, y) in enumerate(coords_list):
            if i < len(marca_values):
                text_value = marca_values[i]
                font_size = 15
                font_name = "Times-Bold"

                wrapped_lines = wrap_text_to_width(text_value, font_name, font_size, box_width)

                total_height = len(wrapped_lines) * (font_size + 2)
                start_y = box_top + (box_height - total_height) / 2

                for j, line in enumerate(wrapped_lines):
                    line_width = fitz.get_text_length(line, fontname=font_name, fontsize=font_size)
                    centered_x = box_left + (box_width - line_width) / 2
                    insert_y = start_y + j * (font_size + 2)

                    page.insert_text(
                        (centered_x, insert_y),
                        line,
                        fontname=font_name,
                        fontsize=font_size,
                        color=(0, 0, 0)
                    )
                print(f"Inserted wrapped Marca value '{text_value}' in {len(wrapped_lines)} lines within box")

    output_path = os.path.join(output_folder, f"{row['NumeroPedido']}.pdf")
    doc.save(output_path)
    doc.close()

    print(f"Saved PDF: {output_path}")

print("All rows processed.")
