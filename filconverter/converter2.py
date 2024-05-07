import fitz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileMerger

def extract_text_from_page(page):
    text = page.get_text()
    return text.strip()

def capitalize_first_two_letters(text):
    words = text.split()
    capitalized_words = [word[:2].upper() + word[2:] for word in words]
    return ' '.join(capitalized_words)

def save_to_pdf(text, output_path, page_number):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    text_lines = text.split('\n')
    page_width, page_height = letter  # Get the width and height of a letter-sized page in points
    margin_left = 50  # Left margin
    margin_right = 50  # Right margin
    margin_top = 50  # Top margin
    margin_bottom = 50  # Bottom margin
    usable_width = page_width - margin_left - margin_right
    usable_height = page_height - margin_top - margin_bottom
    line_height = 15  # Height of each line
    num_lines = len(text_lines)
    lines_per_page = int((usable_height) / line_height)
    
    y = page_height - margin_top  # Starting y-coordinate
    for i, line in enumerate(text_lines):
        lines = [line[i:i+100] for i in range(0, len(line), 100)]  # Wrap text every 100 characters
        for wrapped_line in lines:
            text_width = c.stringWidth(wrapped_line, "Helvetica", 12)
            x = (page_width - text_width) / 2  # Center the text horizontally
            c.drawString(x, y, wrapped_line)
            y -= line_height  # Move to the next line
            if y < margin_bottom:
                c.showPage()  # Start a new page if the text exceeds the page height
                y = page_height - margin_top  # Reset y-coordinate
    c.save()

def merge_pdf_files(input_files, output_file):
    merger = PdfFileMerger()
    for input_file in input_files:
        merger.append(input_file)
    merger.write(output_file)
    merger.close()

def main(input_pdf, output_pdf):
    temp_files = []
    with fitz.open(input_pdf) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            extracted_text = extract_text_from_page(page)
            capitalized_text = capitalize_first_two_letters(extracted_text)
            temp_pdf = f"temp_page_{page_num + 1}.pdf"
            save_to_pdf(capitalized_text, temp_pdf, page_num + 1)
            temp_files.append(temp_pdf)
    merge_pdf_files(temp_files, output_pdf)

if __name__ == "__main__":
    input_pdf = "input.pdf"  # Replace with the path to your input PDF file
    output_pdf = "output.pdf"  # Name of the output PDF file
    main(input_pdf, output_pdf)
