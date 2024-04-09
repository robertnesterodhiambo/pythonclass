import os
from docx import Document as DocxDocument
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import shutil
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_capital(text, image_bytes=None):
    # Capitalize only the first two letters of every word in text content
    words = text.split()
    converted_words = []
    for word in words:
        if len(word) >= 2:
            converted_words.append(word[:2].upper() + word[2:])
        else:
            converted_words.append(word.upper())
    converted_text = ' '.join(converted_words)
    
    # Process image bytes if provided
    if image_bytes:
        # Process image as needed
        pass
    
    return converted_text

def process_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    converted_content = convert_to_capital(content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(converted_content)

def process_docx_file(filepath):
    doc = DocxDocument(filepath)
    image_folder = os.path.join(os.path.dirname(filepath), 'images')
    final_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'images')

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.text = convert_to_capital(run.text)

    for shape in doc.inline_shapes:
        if shape.type == 3:  # Check if the shape is an image
            image_bytes = shape.image.blob
            image_filename = f'image_{shape._inline.graphic.uid}.png'  # Unique filename
            image_path = os.path.join(image_folder, image_filename)
            final_image_path = os.path.join(final_folder, image_filename)
            shutil.copy(image_path, final_image_path)
            shape._inline.graphic.attrib['embed'] = None  # Remove embedding

    # Save the processed document with images inserted
    filename = secure_filename(os.path.basename(filepath))
    new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    doc.save(new_filepath)

import fitz

def process_pdf_file(filepath):
    # Read the PDF file and extract text
    text = ''
    with fitz.open(filepath) as pdf:
        for page in pdf:
            text += page.get_text()
    
    # Process text
    if text.strip():  # Check if the extracted text is not empty
        converted_text = convert_to_capital(text)
        
        # Write the processed text back to the PDF file
        with open(filepath, 'wb') as f:
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.add_page(PyPDF2.PdfFileReader(f))
            pdf_writer.write(f)
    else:
        raise ValueError("Cannot process an empty PDF file")


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
                        process_pdf_file(filepath)
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
