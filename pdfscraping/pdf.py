import fitz  # PyMuPDF
import re

pdf_path = "/home/dragon/Downloads/sinai directory (compressed).pdf"

# Open the PDF
doc = fitz.open(pdf_path)

# Extract text from each page
text = ""
for page in doc:
    text += page.get_text("text") + "\n"

# Define phone number pattern for (XXX) XXX-XXXX format
phone_pattern = re.compile(r"\(\d{3}\) \d{3}-\d{4}")

# Process text line by line
lines = text.split("\n")
processed_text = []
for line in lines:
    processed_text.append(line)
    if phone_pattern.search(line):  # If the line contains (XXX) XXX-XXXX anywhere
        processed_text.append("")  # Add 4 blank lines
        processed_text.append("")
        processed_text.append("")
        processed_text.append("")

# Join the modified text
modified_text = "\n".join(processed_text)

# Save the result
with open("formatted_text.txt", "w", encoding="utf-8") as f:
    f.write(modified_text)

print("Processing complete. Check formatted_text.txt.")
