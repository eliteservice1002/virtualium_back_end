from flask import Flask, request, jsonify, Response, send_file, make_response

from flask_restful import Api
from flask_cors import CORS
import os
import sys

from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static', static_folder="/static")
CORS(app, supports_credentials=True)
api = Api(app)

@app.route('/')
def index():
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

UPLOAD_FOLDER_SOUND = '/var/www/virtualium/virtualium-backend/sound'

app.config['UPLOAD_FOLDER_SOUND'] = UPLOAD_FOLDER_SOUND

ALLOWED_EXTENSIONS_SOUND = set(['mp3', 'wav'])

def allowed_sound(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_SOUND

@app.route('/upload_sound', methods=['POST'])
def upload_sound():
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
            if file and allowed_sound(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_SOUND'], filename))
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

@app.route('/get_sound/<int:number>', methods=['GET'])
def get_sound(number = 0):
    if number > 0:
        file_path = "{}/mix_{}.mp3".format(UPLOAD_FOLDER_SOUND, number)
    else:
        file_path = "{}/mix.mp3".format(UPLOAD_FOLDER_SOUND)

    try:
        response = send_file(file_path, mimetype="audio/mp3")
    except IOError:
        return {'error': 'file not found'}, 404

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"

    return response

@app.route('/get_sounds_count', methods=['GET'])
def get_sounds_count():
   sounds_list = os.listdir(UPLOAD_FOLDER_SOUND)
   sounds_count  = len([sound for sound in sounds_list if 'mix' in sound])
   return {'sounds_count':sounds_count}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)

