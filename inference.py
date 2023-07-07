
import uuid
from PIL import Image

from mmagic.apis import MMagicInferencer

model_name = "deepfillv1"

agic_inferencer = MMagicInferencer(model_name)

class Inferencer():

    def __call__(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        image_path = str(uuid.uuid1()) + ".jpg"
        image.save(image_path)
        mask_path = str(uuid.uuid1()) + ".jpg"
        mask.save(mask_path)
        outputs = agic_inferencer.infer(img=image_path, mask=mask_path)
        
        return Image.fromarray(outputs[1].astype('uint8')).convert('RGB')

inferencer = Inferencer()
