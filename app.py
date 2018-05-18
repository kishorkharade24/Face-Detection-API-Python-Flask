#!flask/bin/python
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
import base64
from io import BytesIO
from PIL import Image

# local imports
from trainer import train_data
from detector import detect_faces
from create_database import create_database_schema

# Constants
UPLOAD_FOLDER = "./dataset"
DATA_FOLDER = "./data"

# Config
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DATA_FOLDER'] = DATA_FOLDER

# Create data directory to upload user photos
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

################################################################
#
#                    APPLICATION ROUTES
#
################################################################


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/detector')
def render_detector():
    return render_template('detect.html')


@app.route('/create-database', methods=['GET'])
def database():
    return create_database_schema()


@app.route('/upload-faces', methods=['POST'])
def up():
    try:
        request_data = request.get_json()
        user_id = request_data['userId']
        connection = sqlite3.connect('database.db')
        c = connection.cursor()
        c.execute('INSERT INTO users (name, emp_id) VALUES (?1, ?2)', (user_id, int(user_id),))
        uid = c.lastrowid
        count = 0
        for file in request_data['files']:
            count = count + 1
            filename = "User." + str(uid) + "." + str(count) + ".png"
            starter = file.find(',')
            image_data = file[starter + 1:]
            image_data = bytes(image_data, encoding="ascii")
            im = Image.open(BytesIO(base64.b64decode(image_data)))
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        connection.commit()
        connection.close()
    except Exception as e:
        print("Exception while uploading faces: ", e)
        return jsonify({'status': "FAILURE", "message":"Unknown error while uploading faces."})

    return jsonify({'status': "SUCCESS", "message": "Uploaded faces successfully."})


@app.route('/upload/<user_id>', methods=['POST'])
def upload(user_id):
    if request.method == 'POST':
        # check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'status': "FAILURE", "message": "No file part found."})
    connection = sqlite3.connect('database.db')
    c = connection.cursor()
    c.execute('INSERT INTO users (name, emp_id) VALUES (?1, ?2)', (user_id, int(user_id),))
    uid = c.lastrowid
    count = 0
    for requestFile in request.files.getlist("file"):
        if requestFile.filename == '':
            return jsonify({'status': "FAILURE", "message": "File not selected."})
        if requestFile:
            count = count + 1
            filename = "User." + str(uid) + "." + str(count) + ".jpg"
            requestFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    connection.commit()
    connection.close()
    return jsonify({'status': "SUCCESS", "message": "Files uploaded successfully."})


@app.route('/train')
def train_face_data():
    return train_data()


@app.route('/detect', methods=['POST'])
def detect():
    if request.method == 'POST':
        print(request)
        if 'file' not in request.files:
            return jsonify({'status': "FAILURE", "message": "No file part found."})
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['DATA_FOLDER'], filename))
    return detect_faces(filename)


@app.route('/detect-face', methods=['POST'])
def detect_face():
    filename = 'face.png'
    try:
        print(request)
        request_data = request.get_json()
        file = request_data['file']
        starter = file.find(',')
        image_data = file[starter + 1:]
        image_data = bytes(image_data, encoding="ascii")
        im = Image.open(BytesIO(base64.b64decode(image_data)))
        im.save(os.path.join(app.config['DATA_FOLDER'], filename))
    except Exception as e:
        print("Exception while detecting faces: ", e)
        return jsonify({"status": "FAILURE", "message": "Unknown error while getting encoded file."})

    return detect_faces(filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)