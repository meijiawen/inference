import uuid
from PIL import Image

from mmagic.apis import MMagicInferencer

# reference: https://github.com/open-mmlab/mmagic/tree/main/configs/controlnet

model_name = "controlnet"
device_id = "cuda:0"

# controlnet-canny
# 如果没有设置device, 优先使用gpu,其次使用cpu
agic_inferencer = MMagicInferencer(model_name, model_setting=1)

class Inferencer():

    def __call__(self, text_prompts, image_control: Image.Image) -> Image.Image:
        image_path = str(uuid.uuid1()) + ".jpg"
        image_control.save(image_path)
        outputs = agic_inferencer.infer(text=text_prompts, control=image_path)
        return outputs[1][0]

inferencer = Inferencer()
