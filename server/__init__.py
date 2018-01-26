from flask import Flask
import os
import sys
sys.path.append('server/goldfish')
UPLOAD_FOLDER = '/tmp/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from server import views
