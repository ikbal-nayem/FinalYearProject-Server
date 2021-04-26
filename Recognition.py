import os
import joblib
from urllib.request import urlopen
from PIL import Image
from face_recognition import preprocessing
from CONF import firebaseConfig, store_token
import pyrebase



class Recognizer():
    def __init__(self):
        firebase = pyrebase.initialize_app(firebaseConfig)
        storage = firebase.storage()
        url = storage.child('model/face_recogniser.pkl').get_url(store_token)
        self.face_recogniser = joblib.load(urlopen(url))
        # file_loc = os.path.dirname(os.path.abspath(__file__))
        # self.face_recogniser = joblib.load(os.path.join(file_loc, 'model', 'face_recogniser.pkl'))
        self.preprocess = preprocessing.ExifOrientationNormalize()


    def recognize(self, img):
        img = img.convert('RGB')
        img = self.preprocess(img)
        faces = self.face_recogniser(img)
        return [{
                'top_prediction': face['top_prediction'],
                'bounding_box': face['bb']
            } for face in faces]


    def recognize_cv2(self, img_array):
        img = Image.fromarray(img_array)
        img = self.preprocess(img)
        faces = self.face_recogniser(img)
        faces_data = [{
                        'top_prediction': face['top_prediction'],
                        'bounding_box': face['bb']
                    } for face in faces]
        return {"faces": faces_data}


    def applyWithURL(self, img_url):
        image = Image.open(urlopen(img_url))
        faces = self.recognize(image)
        return {"faces": faces}


    def applyWithImg(self, img):
        image = Image.open(img)
        faces = self.recognize(image)
        return {"faces": faces}