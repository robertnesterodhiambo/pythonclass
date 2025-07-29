import fitz
import os
import glob
import re
from datetime import datetime


def extract_date_from_filename(path):
    filename = os.path.basename(path)
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d")
    else:
        return datetime.min  # fallback for safety

pdf_pattern = "Boletim_da_PI_-_*.pdf"
pdf_files = glob.glob(pdf_pattern)
if not pdf_files:
    raise FileNotFoundError("No Boletim_da_PI_-_*.pdf files found.")
latest_pdf = max(pdf_files, key=extract_date_from_filename)

# === Create folder for extracted images ===
output_folder = "extracted_image"
os.makedirs(output_folder, exist_ok=True)

def extract_images_columnwise_fixed(pdf_path):
    doc = fitz.open(pdf_path)
    total_saved = 0
    image_counts = {}

    # Preload (210) codes for all pages
    all_codes_per_page = []
    for page in doc:
        width = page.rect.width
        mid_x = width / 2
        blocks = page.get_text("blocks")
        code_210_positions = []
        for b in blocks:
            text = b[4]
            match = re.search(r"\(210\)\s*(\d+)", text)
            if match:
                x, y = b[0], b[1]
                code_210_positions.append((x, y, match.group(1)))
        left = sorted([c for c in code_210_positions if c[0] < mid_x], key=lambda k: -k[1])
        right = sorted([c for c in code_210_positions if c[0] >= mid_x], key=lambda k: -k[1])
        all_codes_per_page.append((left, right))

    # Go page by page
    for page_num in range(len(doc)):
        page = doc[page_num]
        width = page.rect.width
        mid_x = width / 2

        dict_blocks = page.get_text("dict")["blocks"]
        xrefs = [img[0] for img in page.get_images(full=True)]
        xref_index = 0

        for b in dict_blocks:
            if b["type"] == 1:  # image
                img_x, img_y = b["bbox"][0], b["bbox"][1]
                matched_code = None

                left_codes, right_codes = all_codes_per_page[page_num]

                if img_x < mid_x:  # Left column
                    for x, y, code in left_codes:
                        if y < img_y:
                            matched_code = code
                            break
                    if matched_code is None and page_num > 0:
                        prev_right_codes = all_codes_per_page[page_num - 1][1]
                        if prev_right_codes:
                            matched_code = prev_right_codes[0][2]

                else:  # Right column
                    for x, y, code in right_codes:
                        if y < img_y:
                            matched_code = code
                            break
                    if matched_code is None and left_codes:
                        matched_code = left_codes[0][2]

                if matched_code is None:
                    matched_code = f"page{page_num+1}_img{xref_index+1}"

                if xref_index >= len(xrefs):
                    continue
                xref = xrefs[xref_index]
                xref_index += 1

                img_data = doc.extract_image(xref)
                ext = img_data["ext"]
                img_bytes = img_data["image"]

                if matched_code not in image_counts:
                    image_counts[matched_code] = 1
                    filename = f"{matched_code}.{ext}"
                else:
                    image_counts[matched_code] += 1
                    filename = f"{matched_code}_{image_counts[matched_code]}.{ext}"

                full_path = os.path.join(output_folder, filename)
                with open(full_path, "wb") as f:
                    f.write(img_bytes)

                print(f"✅ Saved {full_path}")
                total_saved += 1

    print(f"\n🎉 Done! Extracted {total_saved} image(s) with enhanced image-to-(210) logic.")

# Run
extract_images_columnwise_fixed(latest_pdf)
