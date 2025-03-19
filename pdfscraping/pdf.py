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

# Define the exact unwanted text block to remove (without quotation marks)
unwanted_text = """Note: This Mount Sinai Health Partners (MSHP) Provider Directory displays the specialties under which MSHP providers have elected to 
participate, elected to participate, as well as the health plans with which these providers participate via their Agreements with MSHP.
This Provider Directory also includes the service locations that MSHP has on file as participating sites within its network. Please use
this Provider Search tool to identify providers, their practice locations and their plan participation as dictated by their MSHP 
Agreements."""

# Remove unwanted text from the extracted content
text = text.replace(unwanted_text, "")

# Process text line by line
lines = text.split("\n")
processed_text = []
for line in lines:
    processed_text.append(line)
    if phone_pattern.search(line):  # If the line contains (XXX) XXX-XXXX anywhere
        processed_text.extend(["", "", "", ""])  # Add 4 blank lines

# Join the modified text
modified_text = "\n".join(processed_text)

# Save the result
with open("formatted_text.txt", "w", encoding="utf-8") as f:
    f.write(modified_text)

print("Processing complete. Check formatted_text.txt.")
