# NAMA : HANIFAN HUSEIN ISNANTO (19090006)
# KELAS : 6 C

from crypt import methods
from email.mime import image
from fileinput import filename
from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from enum import unique
from distutils.log import debug
import os
import urllib.request
from werkzeug.utils import secure_filename
from datetime import date, datetime

UPLOAD_FOLDER = 'images'

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "images.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Data(db.Model):
    name = db.Column(db.Text, nullable=False, primary_key=True)
    path = db.Column(db.Text, nullable=False)
    dateTime = db.Column(db.DateTime)

db.create_all()

@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return jsonify({'message': 'Tidak ada request', 'status': 400})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Tidak ada gambar yang dipilih', 'status': 400})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        gambar = Data(name=file.filename, path=UPLOAD_FOLDER, dateTime=datetime.now())
        db.session.add(gambar)
        db.session.commit()
        return jsonify({'message': 'Gambar berhasil diupload', 'status': 200})
    else:
        return jsonify({'message': 'Type file yang diizinkan adalah png, jpg, jpeg'})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
