

from PIL import Image

class Inferencer():

Copy
def __call__(self, image: Image.Image) -> Image.Image:
    return image
inferencer = Inferencer()
