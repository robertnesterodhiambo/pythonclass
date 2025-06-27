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

def extract_boletim_data(pdf_path, output_excel_path):
    pdf_text = extract_text(pdf_path)
    entries = re.split(r"\(210\)", pdf_text)[1:]

    parsed_data = []

    for entry in entries:
        entry = "(210)" + entry
        numero_pedido = re.search(r"\(210\)\s*(\S+)", entry)
        data_pedido = re.search(r"\(220\)\s*(\S+)", entry)
        titular = re.search(r"\(730\)\s*(.+?)(?:\n|\()", entry)
        classe_produtos = re.search(r"\(511\)\s*(\d+)", entry)
        all_marca = re.findall(r"\(540\)\s*(.+?)(?:\n|\(5|\(3|\(7|\(6)", entry)

        marca_text = all_marca[-1].strip() if all_marca else ""
        marca_imagem = all_marca[0].strip() if len(all_marca) > 1 else ""

        parsed_data.append({
            "NumeroPedido": numero_pedido.group(1) if numero_pedido else "",
            "DataPedido": data_pedido.group(1) if data_pedido else "",
            "Titular": titular.group(1).strip() if titular else "",
            "ClasseProdutos": classe_produtos.group(1) if classe_produtos else "",
            "Marca": marca_text,
            "MarcaIM": marca_imagem if marca_imagem != marca_text else "",
        })

    df = pd.DataFrame(parsed_data)
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Extracted {len(df)} entries to Excel: {output_excel_path}")


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

# Download or reuse PDF
if download:
    print("Downloading PDF...")
    response = requests.get(pdf_url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"✅ PDF downloaded as: {filename}")
else:
    print("Using existing PDF:", filename)

# Extract to Excel regardless
extract_boletim_data(filename, excel_filename)

driver.quit()
