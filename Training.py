import os
import joblib
import numpy as np
from PIL import Image
from torchvision import transforms, datasets
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from face_recognition import preprocessing, FaceFeaturesExtractor, FaceRecogniser
from CONF import PRETRAINED_MODEL_PATH

# MODEL_DIR_PATH = 'model'
DATASET_PATH = 'dataset'

trning_status = {
    'total_person': 0,
    'total_image': 0,
    'total_traninged': 0,
    'current_traning': ""
}


def current_status():
    return trning_status

def dataset_to_embeddings(dataset, features_extractor):
    global trning_status
    transform = transforms.Compose([
        preprocessing.ExifOrientationNormalize(),
        transforms.Resize(1024)
    ])

    embeddings = []
    labels = []
    for img_path, label in dataset.samples:
        trning_status['current_traning'] = dataset.classes[label]
        trning_status['total_traninged'] += 1
        print(f'[Training] {img_path}')
        _, embedding = features_extractor(transform(Image.open(img_path).convert('RGB')))
        if embedding is None:
            print("Could not find face on {}".format(img_path))
            continue
        if embedding.shape[0] > 1:
            print("Multiple faces detected for {}, taking one with highest probability".format(img_path))
            embedding = embedding[0, :]
        embeddings.append(embedding.flatten())
        labels.append(label)

    return np.stack(embeddings), labels


def load_data(dataset_path, features_extractor):
    global trning_status
    if not os.path.isdir(dataset_path):
        os.mkdir(dataset_path)
    dataset = datasets.ImageFolder(dataset_path)
    trning_status['total_image'] = len(dataset.imgs)
    trning_status['total_person'] = len(dataset.classes)
    embeddings, labels = dataset_to_embeddings(dataset, features_extractor)
    return embeddings, labels, dataset.class_to_idx


def train(embeddings, labels):
    softmax = LogisticRegression(solver='lbfgs', multi_class='multinomial', C=10, max_iter=10000)
    return softmax.fit(embeddings, labels)


def startTraining():
    global trning_status
    trning_status['total_traninged'] = 0
    features_extractor = FaceFeaturesExtractor()
    embeddings, labels, class_to_idx = load_data(DATASET_PATH, features_extractor)
    clf = train(embeddings, labels)

    idx_to_class = {v: k for k, v in class_to_idx.items()}
    target_names = map(lambda i: i[1], sorted(idx_to_class.items(), key=lambda i: i[0]))
    print(metrics.classification_report(labels, clf.predict(embeddings), target_names=list(target_names)))

    if not os.path.isdir(PRETRAINED_MODEL_PATH.split('/')[0]):
        os.mkdir(PRETRAINED_MODEL_PATH.split('/')[0])
    # model_path = os.path.join(PRETRAINED_MODEL_PATH, 'pretrainedModel.pkl')
    trning_status['current_traning'] = ""
    joblib.dump(FaceRecogniser(features_extractor, clf,
                idx_to_class), PRETRAINED_MODEL_PATH)


if __name__ == '__main__':
    startTraining()
