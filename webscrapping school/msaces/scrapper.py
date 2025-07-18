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
import fitz  # PyMuPDF


def convert_pdf_to_txt_with_images(pdf_path, txt_path):
    print("🔍 Extracting text from PDF...")

    doc = fitz.open(pdf_path)
    text_lines = []
    numero_pedido_for_page = {}

    # Map each page to its first (210) NumeroPedido if available
    for i, page in enumerate(doc):
        text = page.get_text()
        match = re.search(r"\(210\)\s*(\S+)", text)
        if match:
            numero_pedido_for_page[i] = match.group(1)

    for i, page in enumerate(doc):
        rect = page.rect
        mid_x = rect.width / 2

        # Extract left and right columns
        left_text = page.get_text(clip=fitz.Rect(0, 0, mid_x, rect.height))
        right_text = page.get_text(clip=fitz.Rect(mid_x, 0, rect.width, rect.height))

        # Combine column text in reading order
        lines = (left_text + "\n" + right_text).splitlines()
        new_lines = []

        for line in lines:
            line = line.strip()

            # Skip empty or unwanted lines
            if not line:
                continue
            if (
                "BOLETIM DA PROPRIEDADE INDUSTRIAL" in line.upper() or
                re.match(r"^\d+\s+de\s+\d+$", line) or
                re.match(r"^E\s+INDUSTRIAL$", line) or
                re.search(r"N\.º\s+\d{4}/\d{2}/\d{2}", line)
            ):
                continue

            new_lines.append(line)

        text_lines.append("\n".join(new_lines))

    full_text = "\n\n".join(text_lines)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"✅ Text saved: {txt_path}")
    return full_text


def extract_boletim_data_from_string(pdf_text, output_excel_path):
    entries = re.split(r"\(210\)", pdf_text)[1:]
    parsed_data = []

    for entry in entries:
        entry = "(210)" + entry
        numero_pedido = re.search(r"\(210\)\s*(\S+)", entry)
        data_pedido = re.search(r"\(220\)\s*(\S+)", entry)
        classe_produtos = re.search(r"\(511\)\s*(\d+)", entry)

        marca_text = ""
        marca_match = re.search(
            r"\(540\)\s*((?:.|\n)*?)(?=\(\d{3}\)|BOLETIM|N\.º|\d+\s+de\s+\d+|$)",
            entry,
            re.IGNORECASE
        )
        if marca_match:
            marca_value = marca_match.group(1).strip()
            header_footer_pattern = re.compile(r"^E\s+INDUSTRIAL\s+N\.º\s+\d{4}/\d{2}/\d{2}$")
            if header_footer_pattern.match(marca_value):
                marca_value = ""
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

# Convert PDF to .txt (filtered clean text only)
convert_pdf_to_txt_with_images(filename, txt_filename)

# Extract structured fields from .txt
extract_boletim_data_from_txt(txt_filename, excel_filename)

driver.quit()
