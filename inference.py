
from PIL import Image

import numpy as np
from mmpretrain.apis import ImageClassificationInferencer

model_name = "resnet50_8xb32_in1k"

image_inferencer = ImageClassificationInferencer(model_name)

class Inferencer():

    def __call__(self, image: Image.Image):
        return image_inferencer(np.asarray(image))

inferencer = Inferencer()
