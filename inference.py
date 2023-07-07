
from PIL import Image


class Inferencer():

    def __call__(self, image: Image.Image) -> Image.Image:
        return image

inferencer = Inferencer()
