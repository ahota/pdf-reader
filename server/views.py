from server import app

from flask import request, render_template
from werkzeug.utils import secure_filename

import json
import minecart
import os
import redis
import sys

from goldfish.entropy import EntropyWatermarker

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'file' not in request.files:
            return 'no file given'
        result = _get_upload(request.files['file'])
        return json.dumps(result)

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
    wm = EntropyWatermarker()
    candidates = 0
    for image_info in images:
        image_info['message'] = wm.extract(image_info['image_data'],
                message_length=256)
        candidates += 1

    print images
    print candidates, 'candidates found'
    sys.stdout.flush()

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
        _find_watermarks(images)

        # check each watermark against the db
        _check_watermarks(images)

        # return successful results
        watermarked = []
        for i in range(len(images)):
            image_info = images[i]
            if image_info['valid']:
                image_info['image_data'] = ''
                watermarked.append(image_info)
        return watermarked
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
