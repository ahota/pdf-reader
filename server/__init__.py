from flask import Flask
import os
import sys
sys.path.append('server/goldfish')

UPLOAD_DIR = 'pdf_uploads'
if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

app = Flask(__name__)
app.config['UPLOAD_DIR'] = UPLOAD_DIR

from server import views
