import os
from flask import Flask, request
from Recognition import Recognizer
from Training import startTraining, getTraningStatus


app = Flask(__name__)
print('Loading model...')
recognizer = Recognizer()


@app.route('/', methods=['GET'])
def home():
    return "<h1 style='text-align:center;'>Hello world &#128513;!</h1>"


@app.route('/recognize', methods=['GET', 'POST'])
def recognition():
    if request.method == "POST":
        if request.is_json:
            url = request.get_json().get('url', False)
            faces = recognizer.applyWithURL(url) if url else {
                'success': False, 'message': "Image url was not provid into 'url'"}
            return (faces)
        elif request.files:
            img = request.files.get('image', False)
            faces = recognizer.applyWithImg(img) if img else {
                'success': False, 'message': "Image file wasn't provided into 'image'"}
            return (faces)
        else:
            return ({'success': False, 'message': 'Request data should be in JSON format'})
    else:
        return "Recognition server is running..."


@app.route('/train', methods=['GET'])
def train():
    is_training = getTraningStatus()['is_training']
    if request.method == "GET":
        if not is_training:
            startTraining()
        else:
            return getTraningStatus()
        return ({'success': True, 'message': 'Training successful'})


@app.route('/training-status', methods=['GET'])
def training_status():
    return getTraningStatus()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
