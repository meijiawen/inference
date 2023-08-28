
from PIL import Image
import mmdet


class Inferencer():

    def __call__(self, image: Image.Image) -> Image.Image:
        return image

inferencer = Inferencer()
