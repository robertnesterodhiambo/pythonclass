import os
import glob
import pandas as pd
import fitz  # PyMuPDF
import numpy as np
import unicodedata
import re
from datetime import datetime

# === Step 1: Locate Template PDF === 
pdf_path = "Template2.pdf"

# === Step 2: Locate latest Excel file ===
excel_folder = "excel"
list_of_files = glob.glob(os.path.join(excel_folder, '*.xlsx'))

def extract_date_from_filename(path):
    filename = os.path.basename(path)
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    else:
        return datetime.min

latest_excel = max(list_of_files, key=extract_date_from_filename)
print(f"Latest Excel file by date in filename: {latest_excel}")

latest_date = extract_date_from_filename(latest_excel).date()
today_date = datetime.today().date()

if latest_date != today_date:
    print(f"❌ Latest Excel file is dated {latest_date}, but today's date is {today_date}. Exiting script.")
    exit()
else:
    print("✅ Latest Excel file matches today's date. Continuing...")

# === Step 3: Load Excel data ===
df = pd.read_excel(latest_excel)
print(df.head())

# === Step 4: Prepare output folder ===
today_str = today_date.strftime('%Y-%m-%d')
output_folder = f"PDF_{today_str}"

if os.path.exists(output_folder):
    print(f"⚠️ Output folder '{output_folder}' already exists. Files may be overwritten.")
else:
    os.makedirs(output_folder)
    print(f"✅ Created output folder: {output_folder}")

# === Text wrapping helper ===
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

# === Step 5: Process each row ===
for idx, row in df.iterrows():
    marca_value = row['Marca']
    if pd.isna(marca_value) or not str(marca_value).strip():
        print(f"Skipping row {idx+1} with NumeroPedido {row['NumeroPedido']} because Marca is missing or empty")
        continue

    capital_raw = str(row['CapitalSocial']).strip()
    capital_clean = capital_raw.replace("€", "").replace(".", "").replace(",", ".").strip()

    try:
        capital_value = float(capital_clean)
    except ValueError:
        print(f"Skipping row {idx+1} due to invalid CapitalSocial format: '{capital_raw}'")
        continue

    if not (5 < capital_value < 6100):
        print(f"Skipping row {idx+1} because CapitalSocial €{capital_value} is out of range")
        continue

    print(f"Processing row {idx+1} with NumeroPedido: {row['NumeroPedido']}")

    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # Clear borders
        border_thickness = 20
        page.draw_rect(fitz.Rect(0, 0, page.rect.width, border_thickness), color=(1,1,1), fill=(1,1,1), overlay=True)
        page.draw_rect(fitz.Rect(0, page.rect.height - border_thickness, page.rect.width, page.rect.height), color=(1,1,1), fill=(1,1,1), overlay=True)
        page.draw_rect(fitz.Rect(0, 0, border_thickness, page.rect.height), color=(1,1,1), fill=(1,1,1), overlay=True)
        page.draw_rect(fitz.Rect(page.rect.width - border_thickness, 0, page.rect.width, page.rect.height), color=(1,1,1), fill=(1,1,1), overlay=True)

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

                text_value = str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)
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

                if label == "Titular:" and len(text_value) > 40:
                    text_value = text_value[:40] + "\n" + text_value[40:]

                words = text_value.split()
                lines = []
                current_line = ""

                for word in words:
                    if len(current_line + " " + word) <= max_line_length if current_line else len(word) <= max_line_length:
                        current_line += (" " if current_line else "") + word
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
                    lines[1] += " " * (len_first - len_second)

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

        insert_wrapped("Titular:", row['Titular'], shift_left=2, bold=False, leading_spaces=3)
        insert_wrapped("Morada:", row['Morada'], shift_left=2, bold=False, leading_spaces=3)
        insert_after_label("Código Postal:", row['CodigoPostal'], shift_left=2, bold=False, leading_spaces=3)
        insert_after_label("Número do pedido de Registo:", row['NumeroPedido'], skip_line=True, bold=True)
        insert_after_label("Data do Pedido de Registo:", row['DataPedido'], skip_line=True, bold=True)

        validade_inicio = row['ValidadeInicio']
        validade_fim = row['ValidadeFim']
        if pd.notna(validade_inicio) and pd.notna(validade_fim):
            validade_text = f"De {validade_inicio} até {validade_fim}"
            insert_after_label("Validade da Vigilância:", validade_text, skip_line=True, bold=True)
        else:
            print(f"Skipping Validade da Vigilância insertion")

        insert_after_label("Classes de Produtos/Serviços:", row['ClasseProdutos'], skip_line=True, bold=True)
        insert_after_label("Data:", row['DataDocumento'], skip_line=True, bold=True)

        # === Insert full Marca block into predefined area ===
        box_left = 38.97
        box_right = 296.79
        box_top = 293.35
        box_bottom = 525.23
        box_width = box_right - box_left
        box_height = box_bottom - box_top

        full_marca_text = str(marca_value).replace("&amp;", "&").strip()
        font_size = 15
        font_name = "Times-Bold"

        wrapped_lines = wrap_text_to_width(full_marca_text, font_name, font_size, box_width)
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
        print(f"Inserted Marca in {len(wrapped_lines)} lines: {full_marca_text}")

    output_path = os.path.join(output_folder, f"{row['NumeroPedido']}.pdf")
    doc.save(output_path)
    doc.close()
    print(f"Saved PDF: {output_path}")

print("✅ All rows processed.")
