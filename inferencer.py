
from PIL import Image

import numpy as np
from mmdet.apis import DetInferencer


det_inferencer = DetInferencer("faster-rcnn_r50-caffe-c4_1x_coco")


class Inferencer():

    def __call__(self, image: Image.Image,**kwargs) -> Image.Image:
        out = det_inferencer(np.array(image))
        print("first normal arg:", image)
        for key, value in kwargs.items():
            print("{0} = {1}".format(key, value))
        return out

inferencer = Inferencer()
