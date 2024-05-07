import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter

app = Flask(__name__)

UPLOAD_FOLDER = os.path.expanduser('~/mol/pythonclass/filconverter/uploads')
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


def process_pdf_file(filepath):
    with open(filepath, 'rb') as f:
        reader = PdfReader(f)
        writer = PdfWriter()
        for page in reader.pages:
            page_text = page.extract_text()
            page_text_capitalized = convert_to_capital(page_text)
            page_text_capitalized = str(page_text_capitalized)  # Ensure page_text_capitalized is a string
            writer.add_page(page_text_capitalized.encode('latin1'))  # Encode the text to latin1 before adding to writer

        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + secure_filename(os.path.basename(filepath)))
        with open(output_filepath, 'wb') as output_file:
            writer.write(output_file)

        return output_filepath


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
                        # Convert PDF to capitalized PDF
                        output_filepath = process_pdf_file(filepath)
                        return render_template('index.html', message='File converted successfully. <a href="' + output_filepath + '">Download converted file</a>')
                    else:
                        return render_template('index.html', message='PDF file format not supported')

                except Exception as e:
                    return render_template('index.html', message=f'Error processing file: {str(e)}')

            else:
                return render_template('index.html', message='File not found')
        else:
            return render_template('index.html', message='Invalid file format')

    return render_template('index.html', message='')


if __name__ == '__main__':
    app.run(debug=True)
