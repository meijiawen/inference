from transformers import BeitFeatureExtractor, BeitForImageClassification
from urllib.request import urlopen
from PIL import Image
import timm
import torch

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

    def __call__(self, img):
        # files = "./beignets-task-guide.png"
        # img = Image.open(files)

        model = timm.create_model(
            'vit_large_patch14_clip_224.openai_ft_in12k_in1k', pretrained=True)
        model = model.eval()

        # get model specific transforms (normalization, resize)
        data_config = timm.data.resolve_model_data_config(model)
        transforms = timm.data.create_transform(**data_config,
                                                is_training=False)

        output = model(transforms(img).unsqueeze(
            0))  # unsqueeze single image into batch of 1

        top5_probabilities, top5_class_indices = torch.topk(
            output.softmax(dim=1) * 100, k=5)
        print(top5_probabilities, top5_class_indices)

        # image = Image.open(requests.get(imageUrl, stream=True).raw)
        # inputs = feature_extractor(images=image, return_tensors="pt")
        # outputs = model(**inputs)
        # logits = outputs.logits
        # # model predicts one of the 1000 ImageNet classes
        # predicted_class_idx = logits.argmax(-1).item()
        # print("Predicted class:", model.config.id2label[predicted_class_idx])


inferencer = Inferencer()

# import torch
# # from .base import CustomInferencer
# # from .utils import ClassificationResult, ImageType
# from transformers import AutoImageProcessor, ResNetForImageClassification
# from datasets import load_dataset

# model_name = "microsoft/resnet-50"

# # processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
# # model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

# class ImageClassification():

#     def __init__(self):
#         self.processor = AutoImageProcessor.from_pretrained(
#             "microsoft/resnet-50")
#         self.model = ResNetForImageClassification.from_pretrained(
#             "microsoft/resnet-50")

#     def __call__(self, img):
#         inputs = self.processor(img, return_tensors="pt")
#         with torch.no_grad():
#             logits = self.model(**inputs).logits
#         predicted_label = logits.argmax(-1).item()
#         return self.model.config.id2label[predicted_label]

# # dataset = load_dataset("huggingface/cats-image")
# # image = dataset["test"]["image"][0]
# # inferencer = ImageClassification()
# # output = inferencer(img=image)
# # print(output)
