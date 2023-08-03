
from PIL import Image

import numpy as np
from mmpretrain.apis import ImageClassificationInferencer
import os
value=os.environ.get('test')
print(value)
model_name = "resnet50_8xb32_in1k"

image_inferencer = ImageClassificationInferencer(model_name)

def post_process(out):
    out['pred_scores'] = out['pred_scores'].tolist()
    return out

class Inferencer():

    def __call__(self, image: Image.Image,**kwargs):
        outputs = image_inferencer(np.asarray(image))
        print("first normal arg:", image)
        for key, value in kwargs.items():
            print("{0} = {1}".format(key, value))
        return [ post_process(out) for out in outputs]


inferencer = Inferencer()
