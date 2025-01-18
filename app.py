import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
# from pdf2docx import Converter
import pdf2docx as p
import zipfile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def convert():
    if request.method == 'POST':
        f = request.files['file']
        temp_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
        os.makedirs(temp_folder, exist_ok=True)
        docx_files = []
        for pdf_file in pdf_file:
            if pdf_file != '':
                filename = secure_filename(pdf_file)
                pdf_path = os.path.join(temp_folder, filename)
                pdf_file.save(pdf_path)
                docx_path = os.path.join(temp_folder, os.path.splitext(filename[0] + '.docx'))
                converter = p.Converter(pdf_path)
                converter.convert(docx_path, start=0, end=None)
                converter.close()
                docx_files.append(docx_path)

    zip_file = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.files.zip')
    with zipfile.ZipFile(zip_file, 'w') as zip_file:
        for docx_file in docx_files:
            zip_file.write(docx_file,os.path.basename(docx_file))
        return send_file(zip_file, as_attachment=True)
                

if __name__ == '__main__':
    app.run(debug=True)

