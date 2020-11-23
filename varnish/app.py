from flask import Flask, request, jsonify, Response, send_file, make_response
from flask_restful import Api
from flask_cors import CORS
import os
import sys

from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static', static_folder="/static")
CORS(app, supports_credentials=True)
api = Api(app)

@app.route('/selfies')
def index():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

UPLOAD_FOLDER = '/var/www/virtualium/virtualium-backend/images'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAX_CONTENT_LENGTH'] = 120 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'h264', 'png', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if request.method == "POST":
        resp = Response()
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Credentials"] = "true"

        if 'files' not in request.files:
            resp = jsonify({'error' : 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files')

        errors = {}
        success = False

        for file in files:      
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success:
            resp = jsonify({'result':{'success' : 'yes'}})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify({'result':{'success' : 'no'}, 'error' : 'Failed'})
            resp.status_code = 500
            return resp
        return response

@app.route('/get_mosaic', methods=['GET'])
def get_mosaic():
    file_path = "/var/www/virtualium/virtualium-backend/Final.jpg"
    response = send_file(file_path, mimetype="image/gif")

    response = make_response(send_file(file_path, mimetype="image/gif"))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

