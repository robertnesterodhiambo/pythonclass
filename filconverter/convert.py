import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from pdf2docx import Converter
from docx import Document
from docx.shared import Pt
from docx2pdf import convert as convert_to_pdf

app = Flask(__name__)

UPLOAD_FOLDER = os.path.expanduser('~/github/pythonclass/filconverter/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    doc = Document(filepath)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            run.text = convert_to_capital(run.text)
            run.font.size = Pt(12)  # Adjust font size if needed

    doc.save(filepath)


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
                    if filename.endswith('.pdf'):
                        # Convert PDF to DOCX
                        docx_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.docx')
                        cv = Converter(filepath)
                        cv.convert(docx_filepath, start=0, end=None)
                        cv.close()

                        # Capitalize text in DOCX
                        process_docx_file(docx_filepath)

                        # Convert DOCX back to PDF
                        new_pdf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + secure_filename(os.path.basename(filepath)).replace(".pdf", "_capitalized.pdf"))
                        convert_to_pdf(docx_filepath, new_pdf_filepath)

                        # Remove temporary DOCX file
                        os.remove(docx_filepath)

                        return render_template('index.html', message='File converted successfully. <a href="' + new_pdf_filepath + '">Download converted file</a>')
                    elif filename.endswith('.docx'):
                        # Capitalize text in DOCX
                        process_docx_file(filepath)
                        return render_template('index.html', message='File converted successfully.')
                    elif filename.endswith('.txt'):
                        # Capitalize text in TXT
                        process_txt_file(filepath)
                        return render_template('index.html', message='File converted successfully.')
                    else:
                        return render_template('index.html', message='File format not supported')

                except Exception as e:
                    return render_template('index.html', message=f'Error processing file: {str(e)}')

            else:
                return render_template('index.html', message='File not found')
        else:
            return render_template('index.html', message='Invalid file format')

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(debug=True)
