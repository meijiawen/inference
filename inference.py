from urllib.request import urlopen
from PIL import Image
import timm
import torch


def post_process(out):
    out['pred_scores'] = out['pred_scores'].tolist()
    return out


class Inferencer():

    def __init__(self) -> None:
        self.model = timm.create_model(
            'vit_large_patch14_clip_224.openai_ft_in12k_in1k', pretrained=True)
        self.model = self.model.eval()

        # get model specific transforms (normalization, resize)
        self.data_config = timm.data.resolve_model_data_config(self.model)
        self.transforms = timm.data.create_transform(**self.data_config,
                                                     is_training=False)

    def __call__(self, image: Image.Image):

        output = self.model(self.transforms(image).unsqueeze(
            0))  # unsqueeze single image into batch of 1

        top5_probabilities, top5_class_indices = torch.topk(
            output.softmax(dim=1) * 100, k=5)
        print(top5_probabilities, top5_class_indices)
        return top5_probabilities + top5_class_indices


inferencer = Inferencer()
