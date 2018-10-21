#!/usr/bin/env python
import os

from flask import Flask, flash, request, redirect, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
import requests

import transformer

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
FIREBASE_URL = 'https://nickify-dubhacks-2018.firebaseio.com/'
TRANSFORMATIONS = int(requests.get(FIREBASE_URL + 'transformations.json').text)
FACES_SWAPPED = int(requests.get(FIREBASE_URL + 'faces_swapped.json').text)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.context_processor
def inject_stage_and_region():
    return dict(transformations=TRANSFORMATIONS, faces_swapped=FACES_SWAPPED)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
            return redirect(url_for('index', filename=filename))

    fname = request.args.get('filename')
    tfname = request.args.get('transformed_filename')
    return render_template('index.html', filename=fname, transformed_filename=tfname)

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/swapify/<filename>', methods=['POST'])
def swapify(filename):
    return image_transform(filename, 'swapify', 'sw-')

@app.route('/nickify/<filename>', methods=['POST'])
def nickify(filename):
    return image_transform(filename, 'nickify', 'n-')

@app.route('/smilify/<filename>', methods=['POST'])
def smilify(filename):
    return image_transform(filename, 'smilify', 'sm-')

@app.route('/kittify/<filename>', methods=['POST'])
def kittify(filename):
    return image_transform(filename, 'kittify', 'k-')

def image_transform(filename, op, prefix=''):
    global TRANSFORMATIONS
    global FACES_SWAPPED

    TRANSFORMATIONS += 1
    requests.put(FIREBASE_URL + 'transformations.json', data=str(TRANSFORMATIONS))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    transformed_filename = prefix + filename
    transformed_filepath = os.path.join(app.config['UPLOAD_FOLDER'], transformed_filename)
    image, faces_swapped = transformer.transform(filepath, op)
    image.save(transformed_filepath, quality=95)
    FACES_SWAPPED += faces_swapped
    requests.put(FIREBASE_URL + 'faces_swapped.json', data=str(FACES_SWAPPED))

    return redirect(url_for('index', filename=filename, transformed_filename=transformed_filename))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
