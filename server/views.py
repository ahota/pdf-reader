from server import app

from cStringIO import StringIO
from flask import request, render_template, send_from_directory, send_file, redirect
from werkzeug.utils import secure_filename
from pdfminer.pdftypes import PDFNotImplementedError

import json
import minecart
import multiprocessing
import os
import pprint
import redis
import sys

from goldfish.entropy import EntropyWatermarker

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return redirect('/')
    if 'file' not in request.files:
        return 'no file given'
    result = _get_upload(request.files['file'])
    app.config['RESULT'] = result
    return render_template('reader.html')

@app.route('/css/<path:path>')
def style(path):
    return send_from_directory('static/css', path)

@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('static/js', path)

@app.route('/pdfs/<path:path>')
def pdf(path):
    print 'pdf url'
    print path
    sys.stdout.flush()
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], path),
            attachment_filename=app.config['LAST_FILENAME'],
            cache_timeout=0)

@app.route('/overlay_info')
def get_overlay_info():
    return json.dumps(app.config['RESULT'])

def _file_allowed(filename):
    '''
    basic check to see if the filename has an extension and that
    extension is "pdf"
    '''
    base_filename, extension = os.path.splitext(filename)
    return extension and extension.lower() == '.pdf'

def _save_file(infile):
    filename = secure_filename(infile.filename)
    forced_filename = 'last.pdf'
    app.config['LAST_FILENAME'] = filename
    app.config['SAVE_PATH'] = os.path.join(app.config['UPLOAD_FOLDER'],
            forced_filename)
    infile.save(app.config['SAVE_PATH'])
    print app.config['SAVE_PATH']
    sys.stdout.flush()

def _find_images(infile):
    document = minecart.Document(infile)
    if document is None:
        print 'the document is None!'
        sys.stdout.flush()
        return 'document was None'
    images = []
    '''
    for page_num, page in enumerate(document.iter_pages()):
    '''
    page_num = 0
    while True:
        page = document.get_page(page_num)
        if page is None:
            break
        page_num += 1
        for i in page.images:
            image_info = {}
            try:
                image_info['image_data'] = i.as_pil()
            except ValueError as e:
                print 'Got a ValueError, skipping'
            except PDFNotImplementedError:
                print 'Got a PDFNotImplementedError, skipping'
            else:
                image_info['bbox'] = i.get_bbox()
                image_info['page'] = page_num
                image_info['message'] = ''
                image_info['valid'] = False
                image_info['data'] = ''
                images.append(image_info)

    pprint.pprint(images)
    print len(images), 'images found'
    sys.stdout.flush()

    return images

def _do_work(image_info):
    wm = EntropyWatermarker(quality=75,threshold=140000,bits=40)
    image_info['message'] = wm.extract(image_info['image_data'],
            message_length=128)
    return image_info

def _find_watermarks(images):
    candidates = len(images)
    pool = multiprocessing.Pool(min(len(images), 48))
    results = pool.map(_do_work, images)
    pprint.pprint(results)
    print candidates, 'candidates found'
    sys.stdout.flush()
    pool.close()
    pool.join()
    return results

def _check_watermarks(images):
    db = app.config['IMAGE_DB']
    valid = 0
    for image_info in images:
        key = image_info['message'] 
        if key != '':
            data = db.get(key)
            if data is not None:
                image_info['valid'] = True
                image_info['data'] = data
                valid += 1
                print 'found!'
                print data
                sys.stdout.flush()
            else:
                print 'not found'
                sys.stdout.flush()
    print valid, 'valid images found'
    sys.stdout.flush()

def _get_upload(infile):
    if infile and _file_allowed(infile.filename):
        # get and save the pdf (may not be necessary)
        _save_file(infile)

        # use minecart to extract images from the pdf
        images = _find_images(infile)

        # for each image, use a goldfish extractor to get a watermark
        images = _find_watermarks(images)

        # check each watermark against the db
        _check_watermarks(images)

        # return successful results
        watermarked = []
        for i in range(len(images)):
            image_info = images[i]
            if image_info['valid']:
                # convert to base64
                output = StringIO()
                image_info['image_data'].save(output, format='PNG')
                im_data = output.getvalue().encode('base64')
                header = 'data:image/png;base64,' 
                image_info['image_data'] = header + im_data
                sys.stdout.flush()
                watermarked.append(image_info)
        return watermarked
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
