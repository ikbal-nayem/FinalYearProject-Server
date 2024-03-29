def top_prediction(idx_to_class, probs):
    top_label = probs.argmax()
    return {"label": idx_to_class[top_label], "confidence": round(probs[top_label]*100, 1)}


def to_predictions(idx_to_class, probs):
    return [{"label": idx_to_class[i], "confidence": round(prob*100, 1)} for i, prob in enumerate(probs)]


class FaceRecogniser:
    def __init__(self, feature_extractor, classifier, idx_to_class):
        self.feature_extractor = feature_extractor
        self.classifier = classifier
        self.idx_to_class = idx_to_class

    def recognise_faces(self, img):
        bbs, embeddings = self.feature_extractor(img)
        if bbs is None:
            # if no faces are detected
            return []

        predictions = self.classifier.predict_proba(embeddings)

        return [{
                "top_prediction": top_prediction(self.idx_to_class, probs),
                "bb": {"left": bb[0], "top": bb[1], "right": bb[2], "bottom": bb[3]},
                "all_predictions": to_predictions(self.idx_to_class, probs)
            } for bb, probs in zip(bbs, predictions)
        ]

    def __call__(self, img):
        return self.recognise_faces(img)
