from flask import Flask, redirect, render_template, request, session, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask import jsonify, make_response

import os
import uuid

import face_recognition

#serving the flask app
from waitress import serve

app = Flask(__name__)

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
    file_urls = []
    file_encodings = []
    requestId = str(uuid.uuid4())
    
    file_obj = request.files
    print("Files Count:", requestId, len(file_obj))

    if (len(file_obj) != 2):
        return make_response(jsonify(
            id=str(requestId),
            distance=-1,
            code=0
        ), 200)

    for f in file_obj:
        file = request.files.get(f)

        #save the file with to our photos folder
        filename = photos.save(
            file,
            name=requestId + "___" + file.filename
        )
        image = face_recognition.load_image_file("uploads/" + filename)
        image_encoding = face_recognition.face_encodings(image)[0]

        file_encodings.append(image_encoding)

        #append image urls
        file_urls.append(photos.url(filename))

    #Distance
    face_distances = face_recognition.face_distance([file_encodings[0]], file_encodings[1])
    cal_distance = face_distances[0]
    #cal_distance = 0.33

    print("Files:", file_urls)

    return make_response(jsonify(
        id=requestId,
        distance=cal_distance,
        code=1
    ), 200)

if __name__ == "__main__":
   #app.run() ##Replaced with below code to run it using waitress 
   serve(app, host='0.0.0.0', port=8501)
