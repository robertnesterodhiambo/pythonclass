from docx import Document as DocxDocument
from PyPDF2 import PdfReader, PdfWriter
from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

import fitz  # PyMuPDF
from docx import Document as DocxDocument
from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_capital(text):
    # Convert every two letters to capital letters
    converted_text = ''
    for i in range(0, len(text), 2):
        converted_text += text[i:i+2].upper()
    return converted_text

def process_docx(filepath):
    doc = DocxDocument(filepath)
    for paragraph in doc.paragraphs:
        paragraph.text = convert_to_capital(paragraph.text)
    doc.save(filepath)

def process_pdf(filepath):
    doc = fitz.open(filepath)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        converted_text = convert_to_capital(text)
        doc.delete_page(page_num)  # Delete existing page
        new_page = doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_text((0, 0), converted_text)
    doc.save(filepath)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Ensure filename is safe
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the file based on its extension
            try:
                if filename.endswith('.docx'):
                    process_docx(filepath)
                elif filename.endswith('.pdf'):
                    process_pdf(filepath)
            except Exception as e:
                return render_template('index.html', message=f'Error processing file: {str(e)}')
            
            return render_template('view_file.html', filepath=filepath)
        else:
            return render_template('index.html', message='Invalid file format')

    return render_template('index.html', message='')

if __name__ == '__main__':
    app.run(debug=True)

