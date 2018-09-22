import os
import numpy as np
from tensorflow import get_default_graph
from keras.models import model_from_json
from keras.preprocessing import image
from keras import backend as K
from flask import Flask, redirect, request, render_template, flash
from werkzeug.utils import secure_filename

# Define a flask app and some variables
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
MODEL_PATH = 'resnet_1.h5'
UPLOAD_FOLDER = 'uploads'
styles = ['art deco','art nouveau','baroque','louis xiii', 'neoclassical']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Load the model
print('Model loading')
# load architecture and weights separately for speed
json_file = open("model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
# this is necessary for WGSI applications
# see https://github.com/keras-team/keras/issues/2397
model._make_predict_function()
graph = get_default_graph()
print('Model loaded')

# Predict the style of the image
@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no file name!')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file = request.files['file']
            filename = secure_filename(file.filename)
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(img_path)
            img_width, img_height = 256, 256
            img = image.load_img(img_path, target_size=(img_width, img_height))
            img = image.img_to_array(img)
            img = img/255
            img = np.expand_dims(img, axis=0) # to make it nfeature, width, height, channels
            with graph.as_default():
                prediction = model.predict(img)
                prediction = prediction.argmax(axis=-1)[0]
                prediction = styles[prediction]
                flash(prediction)
                os.remove(img_path)
                return redirect(request.url)
    return 'sorry, we should be back soon'

if __name__ == '__main__':
    app.run()

    
