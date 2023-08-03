
from PIL import Image


class Inferencer():

    def __call__(self, images):
        processed_images = []
        for image in images:
            processed_images.append(image)  
        return processed_images

inferencer = Inferencer()

# from PIL import Image

# class Inferencer():

# Copy
# def __call__(self, image: Image.Image) -> Image.Image:
#     return image
# inferencer = Inferencer()
