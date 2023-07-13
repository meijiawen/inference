from transformers import BeitFeatureExtractor, BeitForImageClassification
from PIL import Image
import requests

feature_extractor = BeitFeatureExtractor.from_pretrained(
    'microsoft/beit-base-patch16-384')
model = BeitForImageClassification.from_pretrained(
    'microsoft/beit-base-patch16-384')


class Inferencer():

    # def __init__(self):
    #     self.feature_extractor = BeitFeatureExtractor.from_pretrained(
    #         'microsoft/beit-base-patch16-384')
    #     self.model = BeitForImageClassification.from_pretrained(
    #         'microsoft/beit-base-patch16-384')

    def __call__(self, imageUrl):
        image = Image.open(requests.get(imageUrl, stream=True).raw)
        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)
        logits = outputs.logits
        # model predicts one of the 1000 ImageNet classes
        predicted_class_idx = logits.argmax(-1).item()
        print("Predicted class:", model.config.id2label[predicted_class_idx])


inferencer = Inferencer()
