from flask import Flask, request
from Recognition import applyWithURL, applyWithImg
from Training import startTraining, current_status


training = False

app = Flask(__name__)

@app.route('/recognize', methods=['GET', 'POST'])
def recognizer():
    if request.method == "POST":
        if request.is_json:
            url = request.get_json().get('url', False)
            faces = applyWithURL(url) if url else {'success': False,'message': "Image url was not provid into 'url'"}
            return(faces)
        elif request.files:
            img = request.files.get('image', False)
            faces = applyWithImg(img) if img else {'success': False,'message': "Image file wasn't provided into 'image'"}
            return(faces)
        else:
            return({'success': False, 'message': 'Request data should be in JSON format'})
    else:
        return("Get request in recognizer")


@app.route('/train', methods=['GET'])
def train():
    global training
    if request.method == "GET":
        if not training:
            training = True
            startTraining()
            training = False
        else:
            return(current_status())
        return({'success': True, 'message': 'Training successful'})

@app.route('/training-status', methods=['GET'])
def training_status():
    return(current_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)