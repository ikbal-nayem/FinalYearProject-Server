import os
import shutil
import zipfile
from CONF import DATASET_PATH

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
