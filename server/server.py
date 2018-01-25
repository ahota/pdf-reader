from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import json
import minecart
import os
import sys

UPLOAD_DIR = 'pdf_uploads'
if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'file' not in request.files:
            return 'no file given'
        result = _get_upload(request.files['file'])
        return 'thanks for the file'

def _file_allowed(filename):
    '''
    basic check to see if the filename has an extension and that
    extension is "pdf"
    '''
    base_filename, extension = os.path.splitext(filename)
    return extension and extension.lower() == '.pdf'

def _get_upload(infile):
    if infile and _file_allowed(infile.filename):
        # get and save the pdf
        filename = secure_filename(infile.filename)
        save_path = os.path.join(app.config['UPLOAD_DIR'], filename)
        infile.save(save_path)

        # use minecart to extract images from the pdf

        # for each image, use a goldfish extractor to get a watermark

        # check each watermark against the db

        # return successful results
    return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
