from typing import List

from core import ImageSize
from PIL import Image


class CollageBuilder:
    def build(self, collage_size: ImageSize, images: List[Image.Image]) -> Image:
        pass


class AccurateCollageBuilder(CollageBuilder):

    def build(self, collage_size: ImageSize, images: List[Image.Image]) -> Image:
        image_iter = iter(images)

        next_x = 0
        next_y = 0

        collage_canvas = Image.new('RGB', (collage_size.width, collage_size.height), (250, 250, 250))
        for next_image in image_iter:
            collage_canvas.paste(next_image, (next_x, next_y))

            next_y += ImageSize.from_image(next_image).height

        return collage_canvas
