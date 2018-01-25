from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import json
import minecart
import os
import sys

sys.path.append('goldfish')
from goldfish.watermarker import Watermarker

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
        sys.stdout.flush()
        return 'thanks for the file'

def _file_allowed(filename):
    '''
    basic check to see if the filename has an extension and that
    extension is "pdf"
    '''
    base_filename, extension = os.path.splitext(filename)
    return extension and extension.lower() == '.pdf'

def _save_file(infile):
    filename = secure_filename(infile.filename)
    save_path = os.path.join(app.config['UPLOAD_DIR'], filename)
    infile.save(save_path)

def _find_images(infile):
    document = minecart.Document(infile)
    if document is None:
        print 'the document is None!'
        sys.stdout.flush()
        return 'document was None'
    images = []
    for page_num, page in enumerate(document.iter_pages()):
        for i in page.images:
            image_info = {}
            try:
                image_info['image_data'] = i.as_pil()
            except ValueError as e:
                print 'Got a ValueError, skipping'
            else:
                image_info['bbox'] = i.get_bbox()
                image_info['page'] = page_num
                image_info['message'] = ''
                image_info['valid'] = False
                image_info['data'] = ''
                images.append(image_info)

    print images
    print len(images), 'images found'
    sys.stdout.flush()

    return images

def _find_watermarks(images):
    wm = Watermarker(chan='R', bits_per_pixel=4)
    candidates = 0
    for image_info in images:
        image_info['message'] = wm.extract(image_info['image_data'],
                message_length=600)
        candidates += 1

    print images
    print candidates, 'candidates found'
    sys.stdout.flush()

def _get_upload(infile):
    if infile and _file_allowed(infile.filename):
        # get and save the pdf (may not be necessary)
        _save_file(infile)

        # use minecart to extract images from the pdf
        images = _find_images(infile)

        # for each image, use a goldfish extractor to get a watermark
        _find_watermarks(images)

        # check each watermark against the db

        # return successful results
    return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
