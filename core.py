import errno
import os
from io import BytesIO

import requests
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


def get_image_by_url(url: str) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def create_dir(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
