
from PIL import Image

import numpy as np
from mmdet.apis import DetInferencer


det_inferencer = DetInferencer("faster-rcnn_r50-caffe-c4_1x_coco")


class Inferencer():

    def __call__(self, image: Image.Image) -> Image.Image:
        out = det_inferencer(np.array(image))
        return out

inferencer = Inferencer()
