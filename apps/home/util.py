import os
import requests
import shutil
import zipfile
from CONF import DATASET_PATH, IMAGE_UPLOAD_URL, IMAGE_UPLOAD_TOKEN

dataset_path = os.path.join(os.getcwd(), DATASET_PATH)

def saveDataset(request, id):
    dataset = request.files['dataset']
    if not os.path.isdir(dataset_path):
        os.mkdir(dataset_path)
    _file_path = os.path.join(
        dataset_path, f"{str(id)}.{dataset.filename.split('.')[-1]}")
    dataset.save(_file_path)
    d_path = os.path.join(dataset_path, str(id))
    with zipfile.ZipFile(_file_path, 'r') as zip_ref:
        zip_ref.extractall(d_path)
    os.remove(_file_path)
    return len([entry for entry in os.listdir(d_path) if os.path.isfile(os.path.join(d_path, entry))])


def updateDataset(request, id):
    deleteDataset(id)
    return saveDataset(request, str(id))


def deleteDataset(id):
    current_dataset_path = os.path.join(dataset_path, str(id))
    if os.path.isdir(current_dataset_path):
        shutil.rmtree(current_dataset_path)


def uploadImage(image):
    data = {'key': IMAGE_UPLOAD_TOKEN, 'action': 'upload', 'source': image}
    r = requests.post(IMAGE_UPLOAD_URL, data=data)
    return r.json()['image']


# uploading image and send to the messenger
def sendMessage(admin_mid, image, m_name=None):
    if not admin_mid:
        print("\033[1;33mFaild to send message, No messenger ID found.\033[0;0m")
        return
    print('Sending message to admin...')
    img_str = base64.b64encode(image).decode()
    uploaded_image = uploadImage(img_str)
    if m_name:
        resp = MessageTemplate(admin_mid).generic(title=m_name,
                                                  subtitle="Authorized member",
                                                  image_url=uploaded_image.get(
                                                      "url"),
                                                  buttons=[{'title': 'OK', 'payload': "OK"}])
    else:
        resp = MessageTemplate(admin_mid).generic(title="Do you know?",
                                                  subtitle="An unknown person detected at your doorstep!",
                                                  image_url=uploaded_image.get(
                                                      "url"),
                                                  buttons=[{'title': 'Alarm', 'payload': "ALARM"}, {'title': 'Unlock', 'payload': 'UNLOCK'}])
    print(resp)
