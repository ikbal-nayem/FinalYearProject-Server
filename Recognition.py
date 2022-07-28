import os
import joblib
from urllib.request import urlopen
from PIL import Image
from face_recognition import preprocessing
from CONF import firebaseConfig, store_token, PRETRAINED_MODEL_PATH
import pyrebase


class Recognizer():
    def __init__(self):
        # firebase = pyrebase.initialize_app(firebaseConfig)
        # storage = firebase.storage()
        # url = storage.child('model/face_recogniser.pkl').get_url(store_token)
        # self.face_recogniser = joblib.load(urlopen(url))
        file_loc = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), PRETRAINED_MODEL_PATH)
        if not os.path.exists(file_loc):
            raise Exception(
                f"Pretrained Model not found on the location: {file_loc}")
        self.face_recogniser = joblib.load(file_loc)
        self.preprocess = preprocessing.ExifOrientationNormalize()

    def recognize(self, img):
        img = img.convert('RGB')
        img = self.preprocess(img)
        faces = self.face_recogniser(img)
        return [{
                'top_prediction': face['top_prediction'],
                'bounding_box': face['bb']
                } for face in faces]

    def applyWithURL(self, img_url):
        image = Image.open(urlopen(img_url))
        faces = self.recognize(image)
        return {"faces": faces}

    def applyWithImg(self, img):
        image = Image.open(img)
        faces = self.recognize(image)
        return {"faces": faces}
