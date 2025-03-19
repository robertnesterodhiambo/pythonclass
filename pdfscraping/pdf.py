import fitz  # PyMuPDF

pdf_path = "/home/dragon/Downloads/sinai directory (compressed).pdf"

# Open the PDF
doc = fitz.open(pdf_path)

# Extract text from each page
text = ""
for page in doc:
    text += page.get_text("text") + "\n"

# Split text using horizontal lines
sections = [section.strip() for section in text.split("\n------\n") if section.strip()]

# Save each section separately (optional)
for i, section in enumerate(sections, 1):
    with open(f"section_{i}.txt", "w", encoding="utf-8") as f:
        f.write(section)

print(f"Extracted {len(sections)} sections. Check section_#.txt files.")
