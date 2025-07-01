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

from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import pytesseract


def convert_pdf_to_txt_with_ocr(pdf_path, txt_path):
    print("🔍 Converting PDF to text with OCR fallback...")

    try:
        text = extract_text(pdf_path).strip()
    except Exception as e:
        print("⚠️ extract_text failed:", e)
        text = ""

    if len(text) < 100:
        print("⚠️ Low text detected, applying OCR...")
        ocr_text = []
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image, lang='eng')
            ocr_text.append(f"\n\n--- PAGE {i + 1} ---\n\n" + page_text.strip())
        text = "\n".join(ocr_text)
    else:
        print("✅ PDF text extracted normally.")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Text written to: {txt_path}")
    return text


def extract_boletim_data_from_string(pdf_text, output_excel_path):
    entries = re.split(r"\(210\)", pdf_text)[1:]

    parsed_data = []

    for entry in entries:
        entry = "(210)" + entry
        numero_pedido = re.search(r"\(210\)\s*(\S+)", entry)
        data_pedido = re.search(r"\(220\)\s*(\S+)", entry)
        classe_produtos = re.search(r"\(511\)\s*(\d+)", entry)

        marca_text, marca_imagem = "", ""
        marca_match = re.search(r"\(540\)\s*(.+?)(?=\n|\(\d{3}\))", entry, re.DOTALL)
        if marca_match:
            marca_value = marca_match.group(1).strip()
            if re.search(r"(imagem|figura|logo|gráfico)", marca_value, re.IGNORECASE) or not re.search(r"[a-zA-Z]", marca_value):
                marca_imagem = marca_value
            else:
                marca_text = marca_value

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
            titular_text = re.sub(r"^[A-Z]{2}\s+", "", titular_text)

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

# Step 1: Convert PDF to .txt
convert_pdf_to_txt_with_ocr(filename, txt_filename)

# Step 2: Extract data from .txt
extract_boletim_data_from_txt(txt_filename, excel_filename)

driver.quit()
