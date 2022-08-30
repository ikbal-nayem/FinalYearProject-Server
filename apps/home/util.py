import os
import zipfile

dataset_path = os.path.join(os.getcwd(), 'apps/dataset')


def saveDataset(request, id):
    dataset = request.files['dataset']
    _file_path = os.path.join(
        dataset_path, f"{str(id)}.{dataset.filename.split('.')[-1]}")
    dataset.save(_file_path)
    with zipfile.ZipFile(_file_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(dataset_path, str(id)))
    os.remove(_file_path)
