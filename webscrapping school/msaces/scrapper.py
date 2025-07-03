import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import re
import pandas as pd
from pathlib import Path
import fitz  # PyMuPDF


def convert_pdf_to_txt_with_images(pdf_path, txt_path):
    print("🔍 Extracting text and images per NumeroPedido...")

    image_dir = Path("images")
    image_dir.mkdir(exist_ok=True)

    doc = fitz.open(pdf_path)
    text_lines = []
    numero_pedido_map = {}

    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        blocks = re.split(r"\(210\)", text)
        if len(blocks) <= 1:
            continue  # no entries

        blocks = blocks[1:]  # skip header
        page_entries = ["(210)" + block for block in blocks]

        for block in page_entries:
            lines = block.splitlines()
            entry_lines = []
            numero_pedido = ""
            images_added = []

            for i, line in enumerate(lines):
                if "(210)" in line:
                    match = re.search(r"\(210\)\s*(\S+)", line)
                    if match:
                        numero_pedido = match.group(1)
                    entry_lines.append(line)

                elif "(540)" in line:
                    entry_lines.append(line)
                    marca_text_lines = []
                    j = i + 1
                    while j < len(lines) and not re.match(r"\(\d{3}\)", lines[j]):
                        marca_text_lines.append(lines[j].strip())
                        j += 1

                    # Clean and filter Marca text
                    marca_text_lines = [
                        ln for ln in marca_text_lines
                        if ln and "BOLETIM" not in ln.upper()
                    ]
                    entry_lines.extend(marca_text_lines)

                    # Extract images on this page
                    img_list = page.get_images(full=True)
                    for idx, img in enumerate(img_list):
                        xref = img[0]
                        image_data = doc.extract_image(xref)
                        ext = image_data["ext"]
                        img_bytes = image_data["image"]
                        img_path = image_dir / f"{numero_pedido}.{ext}"
                        with open(img_path, "wb") as f:
                            f.write(img_bytes)
                        entry_lines.append(f"[IMAGE: {img_path.as_posix()}]")
                        images_added.append(img_path.as_posix())
                        break  # only one per NumeroPedido

                    break  # skip to next block after (540)

                else:
                    entry_lines.append(line)

            numero_pedido_map[numero_pedido] = "\n".join(entry_lines)
            text_lines.append("\n".join(entry_lines))

    full_text = "\n\n".join(text_lines)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Text saved: {txt_path}")
    print(f"✅ Images saved to: {image_dir}")
    return full_text


def extract_boletim_data_from_string(pdf_text, output_excel_path):
    entries = re.split(r"\(210\)", pdf_text)[1:]
    parsed_data = []

    for entry in entries:
        entry = "(210)" + entry
        numero_pedido = re.search(r"\(210\)\s*(\S+)", entry)
        data_pedido = re.search(r"\(220\)\s*(\S+)", entry)
        classe_produtos = re.search(r"\(511\)\s*(\d+)", entry)

        marca_text, marca_imagem = "", ""
        marca_match = re.search(r"\(540\)(.*?)(?=\(\d{3}\)|\n{2,}|$)", entry, re.DOTALL)
        if marca_match:
            marca_block = marca_match.group(1).strip()
            marca_lines = marca_block.splitlines()
            img_lines = [line for line in marca_lines if line.strip().startswith("[IMAGE:")]
            text_lines = [
                line.strip()
                for line in marca_lines
                if line.strip()
                and not line.strip().startswith("[IMAGE:")
                and "BOLETIM DA PROPRIEDADE INDUSTRIAL" not in line.upper()
                and "E INDUSTRIAL N.º" not in line.upper()
            ]
            marca_text = " ".join(text_lines)
            marca_imagem = "\n".join(img_lines)

        titular_text = ""
        titular_block = re.search(r"\(730\)(.*?)(?=\(\d{3}\)|BOLETIM|N\.º|\d+\s+de\s+\d+)", entry, re.DOTALL | re.IGNORECASE)
        if titular_block:
            lines = titular_block.group(1).strip().splitlines()
            collected = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                if re.search(r"(BOLETIM|N\.º|\d+\s+de\s+\d+|MNA|PÁGINA\s+\d+)", line, re.IGNORECASE):
                    break
                if re.match(r"\(\d{3}\)", line):
                    break
                collected.append(line)
            titular_text = " ".join(collected)

        parsed_data.append({
            "NumeroPedido": numero_pedido.group(1) if numero_pedido else "",
            "DataPedido": data_pedido.group(1) if data_pedido else "",
            "Titular": titular_text,
            "ClasseProdutos": classe_produtos.group(1) if classe_produtos else "",
            "Marca": marca_text,
            "MarcaIM": marca_imagem,
        })

    def sanitize(value):
        if isinstance(value, str):
            return re.sub(r"[\x00-\x1F\x7F]", " ", value)
        return value

    df = pd.DataFrame(parsed_data)
    df = df.applymap(sanitize)
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Extracted {len(df)} entries to Excel: {output_excel_path}")


def extract_boletim_data_from_txt(txt_path, output_excel_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        pdf_text = f.read()
    extract_boletim_data_from_string(pdf_text, output_excel_path)


# === Selenium logic to detect/download PDF ===
chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://inpi.justica.gov.pt/boletim-da-propriedade-industrial")

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
)

first_wrapper = driver.find_element(By.CLASS_NAME, "wrapper")
link = first_wrapper.find_element(By.TAG_NAME, "a")

driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
time.sleep(1)

pdf_url = link.get_attribute("href")
bulletin_title = link.text.strip().replace(" ", "_").replace(":", "-")
filename = f"{bulletin_title}.pdf"
txt_filename = f"{bulletin_title}.txt"
excel_filename = f"{bulletin_title}.xlsx"

existing_pdfs = [f for f in os.listdir() if f.endswith(".pdf")]
download = False

if not existing_pdfs:
    print("[INFO] No PDF exists. Will download new one.")
    download = True
elif filename in existing_pdfs:
    print("[INFO] PDF already exists. Will use it for extraction.")
    download = False
else:
    print(f"[INFO] New PDF '{filename}' differs from existing file(s): {existing_pdfs}")
    download = True

if download:
    print("Downloading PDF...")
    response = requests.get(pdf_url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ PDF downloaded as: {filename}")
else:
    print("Using existing PDF:", filename)

# Convert PDF to .txt and extract embedded images
convert_pdf_to_txt_with_images(filename, txt_filename)

# Extract structured fields from .txt
extract_boletim_data_from_txt(txt_filename, excel_filename)

driver.quit()
