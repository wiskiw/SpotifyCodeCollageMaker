from typing import List
from PIL import Image
from core import ImageSize

from spotify_utils import DEFAULT_CODE_IMAGE_HEIGHT


class CollageBuilder:
    collage_size = 0
    track_count = 0

    def __init__(self, collage_size: ImageSize, track_count: int):
        self.collage_size = collage_size
        self.track_count = track_count

    def get_code_size(self) -> ImageSize:
        pass

    def build(self, images: List[Image.Image]) -> Image:
        pass


class ColumnCollageBuilder(CollageBuilder):

    def __init__(self, collage_size: ImageSize, track_count: int):
        super(ColumnCollageBuilder, self).__init__(collage_size, track_count)

    def get_code_size(self) -> ImageSize:
        return ImageSize(self.collage_size.width, DEFAULT_CODE_IMAGE_HEIGHT)

    def build(self, images: List[Image.Image]) -> Image:
        image_iter = iter(images)

        next_x = 0
        next_y = 0

        collage_canvas = Image.new('RGB', (self.collage_size.width, self.collage_size.height), (250, 250, 250))
        for next_image in image_iter:
            collage_canvas.paste(next_image, (next_x, next_y))

            next_y += ImageSize.from_image(next_image).height

        return collage_canvas
