import torch
# from .base import CustomInferencer
# from .utils import ClassificationResult, ImageType
from transformers import AutoImageProcessor, ResNetForImageClassification
from datasets import load_dataset

model_name = "microsoft/resnet-50"

# processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
# model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")


class ImageClassification():

    def __init__(self):
        self.processor = AutoImageProcessor.from_pretrained(
            "microsoft/resnet-50")
        self.model = ResNetForImageClassification.from_pretrained(
            "microsoft/resnet-50")

    def __call__(self, img):
        inputs = self.processor(img, return_tensors="pt")
        with torch.no_grad():
            logits = self.model(**inputs).logits
        predicted_label = logits.argmax(-1).item()
        return self.model.config.id2label[predicted_label]


dataset = load_dataset("huggingface/cats-image")
image = dataset["test"]["image"][0]
inferencer = ImageClassification()
output = inferencer(img=image)
print(output)
