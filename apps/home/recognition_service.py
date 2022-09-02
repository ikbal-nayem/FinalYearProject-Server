import json
from algo.Recognition import Recognizer

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
    print(faces)
    return json.dumps(str({"faces": faces}))
