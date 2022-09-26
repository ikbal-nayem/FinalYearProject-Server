import os
import joblib
from urllib.request import urlopen
from PIL import Image
from algo.face_recognition.preprocessing import ExifOrientationNormalize
from CONF import PRETRAINED_MODEL_PATH
# import pyrebase


class Recognizer():
    def __init__(self):
        self.loadModel()
        self.preprocess = ExifOrientationNormalize()

    def loadModel(self):
        self.has_trained = True
        file_loc = os.path.join(os.getcwd(), PRETRAINED_MODEL_PATH)
        if not os.path.exists(file_loc):
            self.has_trained = False
        if self.has_trained:
            self.face_recogniser = joblib.load(file_loc)

    def recognize(self, img):
        img = img.convert('RGB')
        img = self.preprocess(img)
        faces = self.face_recogniser(img)
        return [{
                'top_prediction': face['top_prediction'],
                'bounding_box': face['bb']
                } for face in faces]

    def applyWithURL(self, img_url):
        if self.has_trained:
            image = Image.open(urlopen(img_url))
            return self.recognize(image)

    def applyWithImg(self, img):
        if self.has_trained:
            image = Image.open(img)
            return self.recognize(image)
