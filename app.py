import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
from pdf2docx import Converter
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        # return request.files.getlist('file')
        files = request.files.getlist('file')  # Get the list of uploaded files
        # return files
        temp_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
        os.makedirs(temp_folder, exist_ok=True)
        
        docx_files = []

        for pdf_file in files:
            if pdf_file.filename != '':
                filename = secure_filename(pdf_file.filename)
                pdf_path = os.path.join(temp_folder, filename)
                pdf_file.save(pdf_path)

                docx_path = os.path.join(temp_folder, os.path.splitext(filename)[0] + '.docx')

                converter = Converter(pdf_path)
                converter.convert(docx_path, start=0, end=None)
                converter.close()

                docx_files.append(docx_path)

        zip_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_files.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for docx_file in docx_files:
                zipf.write(docx_file, os.path.basename(docx_file))

        return send_file(zip_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
