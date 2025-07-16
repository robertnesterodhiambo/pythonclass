import os
import glob
import subprocess

# === Step 1: Locate the latest Boletim_da_PI_-_YYYY-MM-DD.pdf ===
pdf_pattern = "Boletim_da_PI_-_*.pdf"
pdf_files = glob.glob(pdf_pattern)

if not pdf_files:
    print("No Boletim_da_PI PDF file found in current directory.")
    exit(1)

# Sort by modified time descending to get the latest
pdf_files.sort(key=os.path.getmtime, reverse=True)
latest_pdf = os.path.abspath(pdf_files[0])
print(f"Latest PDF found: {latest_pdf}")

# === Step 2: Prepare output HTML file name ===
output_html = os.path.splitext(latest_pdf)[0] + ".html"

# === Step 3: Convert using pdf2htmlEX ===
try:
    subprocess.run(["pdf2htmlEX", latest_pdf, output_html], check=True)
    print(f"Conversion completed: {output_html}")

except subprocess.CalledProcessError as e:
    print("Conversion failed:", e)
