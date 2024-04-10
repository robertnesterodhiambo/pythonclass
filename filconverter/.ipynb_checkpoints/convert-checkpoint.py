import os
from docx import Document as DocxDocument
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import shutil
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
import PyPDF2


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_capital(text):
    # Capitalize only the first two letters of every word in text content
    words = text.split()
    converted_words = []
    for word in words:
        if len(word) >= 2:
            converted_words.append(word[:2].upper() + word[2:])
        else:
            converted_words.append(word.upper())
    return ' '.join(converted_words)

def process_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    converted_content = convert_to_capital(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(converted_content)

def process_docx_file(filepath):
    doc = DocxDocument(filepath)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.text = convert_to_capital(run.text)

    # Save the processed document
    filename = secure_filename(os.path.basename(filepath))
    new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    doc.save(new_filepath)

    # Copy all related files (like images) to the new location
    original_dir = os.path.dirname(filepath)
    new_dir = os.path.dirname(new_filepath)
    for rel_item in os.listdir(original_dir):
        rel_item_path = os.path.join(original_dir, rel_item)
        if os.path.isfile(rel_item_path) and rel_item != filename:
            shutil.copy(rel_item_path, new_dir)

def process_pdf_file(filepath):
    # Convert each page of the PDF to images
    images = convert_from_path(filepath)

    # Create a new PDF
    filename = secure_filename(os.path.basename(filepath))
    new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + filename)
    doc = SimpleDocTemplate(new_filepath, pagesize=letter)

    # Insert images into the PDF
    elements = []
    for image in images:
        elements.append(Image(image, width=letter[0], height=letter[1]))

    doc.build(elements)

    return new_filepath

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file part')
        
        file = request.files['file']
        
        if file.filename == '':
            return render_template('index.html', message='No selected file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if os.path.exists(filepath):
                try:
                    if filename.endswith('.txt'):
                        process_txt_file(filepath)
                    elif filename.endswith('.docx'):
                        process_docx_file(filepath)
                    elif filename.endswith('.pdf'):
                        new_filepath = process_pdf_file(filepath)
                        return render_template('index.html', message='File converted successfully. <a href="' + new_filepath + '">Download converted file</a>')
                    else:
                        return render_template('index.html', message='File format not supported')
                    
                    return render_template('index.html', message='File converted successfully')
                
                except Exception as e:
                    return render_template('index.html', message=f'Error processing file: {str(e)}')
                
            else:
                return render_template('index.html', message='File not found')
        else:
            return render_template('index.html', message='Invalid file format')

    return render_template('index.html', message='')

if __name__ == '__main__':
    app.run(debug=True)
