import os
import pandas as pd
import pdfkit  # Make sure wkhtmltopdf is installed

# === Step 1: Find latest Excel file ===
excel_folder = 'excel'
files = [os.path.join(excel_folder, f) for f in os.listdir(excel_folder) if f.endswith(('.xls', '.xlsx'))]
latest_file = max(files, key=os.path.getctime)
print(f"Using latest Excel file: {latest_file}")

# === Step 2: Read Excel file ===
columns_needed = [
    "NumeroPedido", "Titular", "Morada", "CodigoPostal", "ClasseProdutos",
    "ValorImportancia", "IVA", "ValorTotal", "MontanteMB", "ReferenciaMB", "EntidadeMB"
]
df = pd.read_excel(latest_file, usecols=columns_needed)

# === Step 3: Read the base HTML ===
with open("Report.html", "r", encoding="utf-8") as file:
    base_html = file.read()

# === Step 4: Generate PDF per row ===
output_dir = "PDF"
os.makedirs(output_dir, exist_ok=True)

for idx, row in df.iterrows():
    filled_html = base_html
    values = [
        row.get("Titular", ""),
        row.get("Morada", ""),
        row.get("CodigoPostal", ""),
        row.get("NumeroPedido", ""),
        "",  # Data do Pedido de Registo
        row.get("ClasseProdutos", ""),
        "",  # Validade da Vigilância
        "",  # Data
        row.get("ValorImportancia", ""),
        row.get("IVA", ""),
        row.get("ValorTotal", ""),
        row.get("EntidadeMB", ""),
        row.get("ReferenciaMB", ""),
        row.get("MontanteMB", "")
    ]

    # Replace each #Name? occurrence with a value
    for value in values:
        filled_html = filled_html.replace("#Name?", str(value), 1)

    output_path = os.path.join(output_dir, f"filled_form_{idx + 1}.pdf")
    pdfkit.from_string(filled_html, output_path)
    print(f"Generated: {output_path}")
