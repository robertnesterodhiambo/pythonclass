import os
import glob
import fitz  # PyMuPDF

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
output_html = os.path.splitext(latest_pdf)[0] + "_stacked_columns.html"

# === Step 3: Open PDF and extract columns ===
doc = fitz.open(latest_pdf)

left_column_texts = []
right_column_texts = []

for page_num, page in enumerate(doc, start=1):
    rect = page.rect
    # Define left and right column rectangles (split page vertically)
    left_rect = fitz.Rect(rect.x0, rect.y0, rect.x0 + rect.width / 2, rect.y1)
    right_rect = fitz.Rect(rect.x0 + rect.width / 2, rect.y0, rect.x1, rect.y1)
    
    left_text = page.get_textbox(left_rect).strip()
    right_text = page.get_textbox(right_rect).strip()
    
    left_column_texts.append(left_text)
    right_column_texts.append(right_text)

# === Step 4: Create HTML content stacking left column text first, then right column text ===
html_content = "<html><head><meta charset='utf-8'><title>Stacked Columns</title></head><body>"

html_content += "<h2>Left Column Text (all pages)</h2>"
for page_num, text in enumerate(left_column_texts, start=1):
    html_content += f"<h3>Page {page_num}</h3>"
    html_content += f"<p>{text.replace(chr(10), '<br>')}</p>"

html_content += "<hr>"

html_content += "<h2>Right Column Text (all pages)</h2>"
for page_num, text in enumerate(right_column_texts, start=1):
    html_content += f"<h3>Page {page_num}</h3>"
    html_content += f"<p>{text.replace(chr(10), '<br>')}</p>"

html_content += "</body></html>"

# === Step 5: Save HTML ===
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML file with stacked columns created: {output_html}")
