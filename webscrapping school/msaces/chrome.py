import os
import time
import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from unidecode import unidecode

# Auto-install ChromeDriver
chromedriver_autoinstaller.install()

# Paths
current_folder = os.path.dirname(os.path.abspath(__file__))
xlsx_files = [f for f in os.listdir(current_folder) if f.endswith('.xlsx') and not f.startswith("~$")]

if not xlsx_files:
    print("❌ No .xlsx file found in the folder.")
    exit()

input_path = os.path.join(current_folder, xlsx_files[0])
output_path = os.path.join(current_folder, "racius_links_output.xlsx")

# Load input Excel
input_df = pd.read_excel(input_path).dropna(how='all')
if 'Titular' not in input_df.columns:
    print("❌ 'Titular' column missing in Excel.")
    exit()

# Prepare output DataFrame
extra_cols = [
    'Link', 'NIF', 'Morada', 'CodigoPostal', 'ValidadeInicio', 'ValidadeFim', 'DataDocumento',
    'ValorImportancia', 'IVA', 'ValorTotal', 'MontanteMB', 'ReferenciaMB', 'EntidadeMB'
]
if os.path.exists(output_path):
    output_df = pd.read_excel(output_path)
else:
    output_df = pd.DataFrame(columns=list(input_df.columns) + extra_cols)

# Set up dates
now = datetime.now()
validade_inicio = now.strftime("%m/%Y")
validade_fim = (now + relativedelta(years=10)).strftime("%m/%Y")
data_documento = now.strftime("%Y-%m-%d")

# Start auto-increment values
ref_start = 123456789
entidade_start = 12345
next_ref = ref_start + len(output_df)
next_ent = entidade_start + len(output_df)

# Selenium setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

driver.get("https://www.racius.com/")

# Iterate rows
for idx, row in input_df.iterrows():
    name_full = str(row['Titular']).strip()
    print(f"\n🔍 Searching for: {name_full}")

    try:
        # Search
        search_input = wait.until(EC.element_to_be_clickable((By.ID, "main-search")))
        search_input.clear()
        search_input.send_keys(name_full)
        search_input.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row.results")))
        time.sleep(2)

        matched = False
        result_divs = driver.find_elements(By.CSS_SELECTOR, "div.col--one")

        for div in result_divs:
            try:
                name_tags = div.find_elements(By.CSS_SELECTOR, "p.results__name")
                if not name_tags:
                    continue
                name_text = name_tags[0].text.strip()

                # ✅ Clean Excel text
                titular_cleaned = re.sub(r'[,.]', '', name_full).strip()
                titular_cleaned = re.sub(r'\blda\b$', '', titular_cleaned, flags=re.IGNORECASE).strip()
                titular_normalized = unidecode(titular_cleaned).lower()

                # ✅ Clean website text
                website_cleaned = re.sub(r'[,.]', '', name_text).strip()
                website_cleaned = re.sub(r'\blda\b$', '', website_cleaned, flags=re.IGNORECASE).strip()
                website_normalized = unidecode(website_cleaned).lower()

                # ✅ Check exact match
                if website_normalized == titular_normalized:
                    matched = True

                # ✅ Exception handling: Excel has no dash but website has
                elif '-' in website_normalized and '-' not in titular_normalized:
                    website_no_dash = website_normalized.replace('-', '').replace('  ', ' ').strip()
                    if website_no_dash == titular_normalized:
                        matched = True

                if matched:
                    result_link = div.find_element(By.CSS_SELECTOR, "a.results__col-link")
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", result_link)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", result_link)

                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
                    time.sleep(2)

                    current_link = driver.current_url
                    print(f"✅ Matched and got link: {current_link}")

                    # Extract NIF
                    try:
                        nif_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.company__loc h3.company-info__data")))
                        nif = nif_element.text.strip()
                    except:
                        nif = ""

                    # Extract Morada and CodigoPostal
                    try:
                        morada_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.t--d-blue")))
                        full_address = morada_element.text.strip()

                        match = re.search(r'\d{4}-\d{3}(.*?)$', full_address)
                        codigo_postal = match.group().strip() if match else ""
                        morada = full_address.split(match.group())[0].strip(', ') if match else full_address
                    except:
                        morada = ""
                        codigo_postal = ""

                    # Extract ValorImportancia
                    try:
                        li_elements = driver.find_elements(By.CSS_SELECTOR, "li.d--flex.detail__detail.py-md--1.align--center")
                        if len(li_elements) >= 2:
                            valor_tag = li_elements[1].find_element(By.CSS_SELECTOR, "p.t--d-blue")
                            valor_text = valor_tag.text.strip().replace("€", "").replace(",", ".")
                            valor_importancia = float(re.search(r'[\d.]+', valor_text).group())
                        else:
                            valor_importancia = 0.0
                    except:
                        valor_importancia = 0.0

                    iva = round(valor_importancia * 0.23, 2)
                    valor_total = round(valor_importancia + iva, 2)
                    montante_mb = valor_total

                    referencia_mb = str(next_ref).zfill(9)
                    entidade_mb = str(next_ent).zfill(5)
                    next_ref += 1
                    next_ent += 1

                    output_row = row.to_dict()
                    output_row.update({
                        'Link': current_link,
                        'NIF': nif,
                        'Morada': morada,
                        'CodigoPostal': codigo_postal,
                        'ValidadeInicio': validade_inicio,
                        'ValidadeFim': validade_fim,
                        'DataDocumento': data_documento,
                        'ValorImportancia': valor_importancia,
                        'IVA': iva,
                        'ValorTotal': valor_total,
                        'MontanteMB': montante_mb,
                        'ReferenciaMB': referencia_mb,
                        'EntidadeMB': entidade_mb
                    })

                    output_df = pd.concat([output_df, pd.DataFrame([output_row])], ignore_index=True)
                    output_df.to_excel(output_path, index=False)
                    break
            except Exception as e:
                print(f"⚠️ Error checking result: {e}")
                continue

        if not matched:
            print(f"❌ No exact match for: {name_full}")
            output_row = row.to_dict()
            for col in extra_cols:
                output_row[col] = "Not Found"
            output_df = pd.concat([output_df, pd.DataFrame([output_row])], ignore_index=True)
            output_df.to_excel(output_path, index=False)

        driver.get("https://www.racius.com/")
        time.sleep(2)

    except Exception as e:
        print(f"🚫 Error with search '{name_full}': {e}")
        driver.get("https://www.racius.com/")
        time.sleep(2)

driver.quit()
print(f"\n✅ Finished. All links and data saved in: {output_path}")
