from flask import Flask, redirect, render_template, request, session, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask import jsonify, make_response

import os
import uuid

import face_recognition

#serving the flask app
from waitress import serve
from logging.config import fileConfig

app = Flask(__name__)
fileConfig('logging.cfg')

app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/distance',methods=['POST'])
def distance():

    requestId = str(uuid.uuid4())
    try:    
        print("Inc request")
        file_urls = []
        file_encodings = []
        
        file_obj = request.files
        app.logger.info('Request received for id %s with number of image %d', requestId, len(file_obj))

        if (len(file_obj) != 2):
            json_response = jsonify(id=requestId,distance=-1,code=0)
            app.logger.error('ID: %s response with code 0 FAILED: number of files uploaded %d', requestId, len(file_obj))
            return make_response(json_response, 200)

        all_files = []
        for f in file_obj:
            file = request.files.get(f)

            #save the file with to our photos folder
            filename = photos.save(
                file,
                name=requestId + "___" + file.filename
            )

            all_files.append(filename)


        for filename in all_files:

            image = face_recognition.load_image_file("uploads/" + filename)

            #from encoding pick first face else return with -1
            image_encoding = face_recognition.face_encodings(image)
            if (len(image_encoding) < 1):
                json_response = jsonify(id=requestId,distance=-1,code=0)
                app.logger.error('ID: %s response code 0 FAILED: image with NO_FACE_DETECTED %s',requestId,photos.url(filename))
                return make_response(json_response, 200)

            file_encodings.append(image_encoding[0])

            #append image urls
            file_urls.append(photos.url(filename))

        #Distance
        face_distances = face_recognition.face_distance([file_encodings[0]], file_encodings[1])
        cal_distance = face_distances[0]
        #cal_distance = 0.33

        #print("Files:", file_urls)

        json_response = jsonify(id=requestId,distance=cal_distance,code=1)
        app.logger.info('ID: %s response code 1 SUCCESS: distance %d with image1: %s image2: %s',requestId,cal_distance,file_urls[0], file_urls[1])
        return make_response(json_response, 200)
    except Exception:
        app.logger.exception('ID: %s response code 0 FAILED: exception in code', requestId)
        return make_response(jsonify(id=requestId,distance=-1,code=0), 200)


if __name__ == "__main__":
   #app.run() ##Replaced with below code to run it using waitress 
   serve(app, host='0.0.0.0', port=8501)
