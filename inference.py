
from PIL import Image

import numpy as np
from mmpretrain.apis import ImageClassificationInferencer

model_name = "resnet50_8xb32_in1k"

image_inferencer = ImageClassificationInferencer(model_name)

def post_process(out):
    out['pred_scores'] = out['pred_scores'].tolist()
    return out

class Inferencer():

    def __call__(self, image: Image.Image):
        outputs = image_inferencer(np.asarray(image))
        
        return [ post_process(out) for out in outputs]


inferencer = Inferencer()
