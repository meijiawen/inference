
from PIL import Image

import numpy as np
from mmdet.apis import DetInferencer


det_inferencer = DetInferencer("faster-rcnn_r50-caffe-c4_1x_coco")


class Inferencer():

    def __call__(self, image: Image.Image,**kwargs) -> Image.Image:
        print("first normal arg:", image)
        for key, value in kwargs.items():
            print("{0} = {1}".format(key, value))
        out = det_inferencer(np.array(image), return_vis=return_visualization)
        predictions = out['predictions'][0]
        return_visualization = kwargs.pop("return_visualization", False)
        print(return_visualization)
        
        vis = ""
        if len(out['visualization']) > 0:
            vis = array_to_base64(out['visualization'][0])

        return DetectionResult(labels=predictions['labels'], 
                               scores=predictions['scores'], 
                               bboxes=predictions['bboxes'], 
                               masks=predictions['masks'], 
                               poses=None,
                               visualization=vis)
        
inferencer = Inferencer()
