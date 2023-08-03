
from PIL import Image


class Inferencer():

    def __call__(self, image: Image.Image) -> Image.Image:
        processed_images = []
        for image in images:
            processed_images.append(image)  
        return processed_images

inferencer = Inferencer()
