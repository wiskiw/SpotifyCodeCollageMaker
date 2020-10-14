from PIL import Image


class ImageSize:

    @staticmethod
    def from_image(image: Image):
        return ImageSize(image.size[0], image.size[1])

    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return "ImageSize(w:" + str(self.width) + "; h" + str(self.height) + ")"
