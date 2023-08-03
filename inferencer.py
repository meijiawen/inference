import base64
from io import BytesIO
from PIL import Image
from dataclasses import dataclass
from typing import Optional, List

import numpy as np
from mmdet.apis import DetInferencer


det_inferencer = DetInferencer("mask-rcnn_r50_fpn_gn-all_2x_coco")


@dataclass
class InstanceMask:
    """The dataclass of the instance segmentation mask."""
    size: List[int]  # The size of the mask
    counts: str  # The RLE-encoded mask


@dataclass
class InstancePose:
    """The dataclass of the pose (keypoint) information of an object."""
    keypoints: List[List[float]]  # The coordinates of all keypoints
    keypoint_scores: Optional[List[float]]  # The scores of all keypoints


@dataclass
class DetectionResult:
    """The result of object detection."""
    # The bounding boxes of all detected objects
    bboxes: Optional[List[List[int]]]
    # The labels of all detected objects
    labels: Optional[List[int]]
    # The scores of all detected objects
    scores: Optional[List[float]]
    # The segmentation masks of all detected objects
    masks: Optional[List[InstanceMask]]
    # The pose estimation results of all detected objects
    poses: Optional[List[InstancePose]]
    # visualization
    visualization: Optional[str]


def array_to_base64(img_array):
    """ndarray转为图片（base64）"""
    img_byte = BytesIO()
    img = Image.fromarray(img_array)
    img.save(img_byte, format="jpeg")

    return base64.b64encode(img_byte.getvalue()).decode('utf-8')


class Inferencer():

    def __call__(self, image: Image.Image, **kwargs) -> Image.Image:
        print(kwargs)
        return_visualization = kwargs.pop("return_visualization", False)
        out = det_inferencer(np.array(image), return_vis=return_visualization)
        predictions = out['predictions'][0]

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
