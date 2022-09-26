import math
import threading
from CONF import MIN_CONFIDENCE_LEVEL
from algo.Recognition import Recognizer
from apps.authentication.models import Users
from .models import Members
from .service import setEntryLog
from .util import sendMessage


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

    user_id = None
    image = None
    notify_admin = False

    if request.is_json:
        url = request.get_json().get('url', False)
        user_id = request.get_json().get('user_id', False)
        if not url:
            # No image URL found
            return ({'success': False, 'message': "Image url wasn't provided into 'url'"})
        try:
            faces = recognizer.applyWithURL(url)
        except ValueError:
            return ({'success': False, 'message': "Please provide a valid 'url'"})

    elif request.files:
        img = request.files.get('image', False)
        user_id = request.form.get('user_id', False)
        notify_admin = request.form.get('notify_admin', False)
        if not img:
            # No image file found
            return ({'success': False, 'message': "Image file wasn't provided into 'image'"})
        image = img.read()
        faces = recognizer.applyWithImg(img)

    if faces:
        big_face = findBigFace(faces)
        admin = Users.query.filter_by(id=user_id).first()
        if big_face['top_prediction'].get('confidence') >= MIN_CONFIDENCE_LEVEL:
            # If authorized member found
            member = Members.query.filter_by(
                id=big_face['top_prediction'].get('label')).first()
            resp = {**big_face, 'isAuthorized': True,
                    "member": member.as_dict() if member else None}
            m_name = f'{member.first_name} {member.last_name}'
            setEntryLog(user_id, m_name, 'Auto',
                        resp['top_prediction'].get('confidence'))
            if admin:
                threading.Thread(target=sendMessage, args=(
                    admin.m_id, image, m_name)).start()  # Sending message
            return resp
        else:
            # If authorized member not found
            if admin and notify_admin == "True":
                threading.Thread(target=sendMessage, args=(
                    admin.m_id, image)).start()  # Sending message
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
