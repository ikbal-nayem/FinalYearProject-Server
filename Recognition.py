import os
import joblib
import urllib.request as request
from PIL import Image
from face_recognition import preprocessing


file_loc = os.path.dirname(os.path.abspath(__file__))
face_recogniser = joblib.load(os.path.join(file_loc, 'model', 'face_recogniser.pkl'))
preprocess = preprocessing.ExifOrientationNormalize()


def recognize(img):
    img = img.convert('RGB')
    img = preprocess(img)
    faces = face_recogniser(img)
    return [{
            'top_prediction': face['top_prediction'],
            'bounding_box': face['bb']
        } for face in faces]

def recognize_cv2(img_array):
    img = Image.fromarray(img_array)
    img = preprocess(img)
    faces = face_recogniser(img)
    faces_data = [{
                    'top_prediction': face['top_prediction'],
                    'bounding_box': face['bb']
                } for face in faces]
    return {"faces": faces_data}

def applyWithURL(img_url):
    image = Image.open(request.urlopen(img_url))
    faces = recognize(image)
    return {"faces": faces}


def applyWithImg(img):
    image = Image.open(img)
    faces = recognize(image)
    return {"faces": faces}