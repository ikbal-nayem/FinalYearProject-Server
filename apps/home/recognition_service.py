import json
import math
from apps import db
from flask_login import current_user
from CONF import MIN_CONFIDENCE_LEVEL
from algo.Recognition import Recognizer
from .models import Members
from .service import setEntryLog

print('Loading model...')
recognizer = Recognizer()


def reloadModel():
  recognizer.loadModel()


def isModelTrained():
  return recognizer.has_trained


def checkRequestImage(request):
  if not recognizer.has_trained:
    # Model is not ready
    return {"success": False, "message": "Dataset was not trained yet"}

  if not request.is_json and not request.files:
    # No request body found
    return ({'success': False, 'message': "Please provide a JSON with image URL on 'url' or direct image file on 'image' parameter"})

  if request.is_json:
    url = request.get_json().get('url', False)
    if not url:
      # No image URL found
      return ({'success': False, 'message': "Image url wasn't provided into 'url'"})
    try:
      faces = recognizer.applyWithURL(url)
    except ValueError:
      return ({'success': False, 'message': "Please provide a valid 'url'"})

  elif request.files:
    img = request.files.get('image', False)
    if not img:
      # No image file found
      return ({'success': False, 'message': "Image file wasn't provided into 'image'"})
    faces = recognizer.applyWithImg(img)

  if faces:
    big_face = findBigFace(faces)
    if big_face['top_prediction'].get('confidence') >= MIN_CONFIDENCE_LEVEL:
      # Do something after authentication
      member = Members.query.filter_by(
          id=big_face['top_prediction'].get('label')).first()
      resp = {**big_face, 'isAuthorized': True,
              "member": member.as_dict() if member else None}
      setEntryLog(f'{member.first_name} {member.last_name}', 'Auto',
                  resp['top_prediction'].get('confidence'))
      return resp
    return ({**big_face, 'isAuthorized': False})
  return ({'success': True, 'message': "No face found in the picture"})


# Finding front face on the given picture (if any)
def findBigFace(faces):
  res = faces[0]
  max_dist = 0
  for face in faces:
    face['bounding_box']['left'] = round(face['bounding_box']['left'])
    face['bounding_box']['top'] = round(face['bounding_box']['top'])
    face['bounding_box']['right'] = round(face['bounding_box']['right'])
    face['bounding_box']['bottom'] = round(face['bounding_box']['bottom'])
    f_dis = math.dist((face['bounding_box']['left'], face['bounding_box']['top']), (
        face['bounding_box']['right'], face['bounding_box']['bottom']))
    if f_dis > max_dist:
      res = face
  return res
