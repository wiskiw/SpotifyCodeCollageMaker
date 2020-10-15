from typing import List
from PIL import Image
from core import ImageSize


class CollageBuilder:
    _collage_size = 0
    _track_count = 0

    def __init__(self, collage_size: ImageSize, track_count: int):
        self._collage_size = collage_size
        self._track_count = track_count

    def build(self, images: List[Image.Image]) -> Image:
        pass


class SingleSizeColumnCollageBuilder(CollageBuilder):
    _code_size: ImageSize
    _column_number: int

    def __init__(self, collage_size: ImageSize, code_size: ImageSize, track_count: int, column_number: int = 1):
        super(SingleSizeColumnCollageBuilder, self).__init__(collage_size, track_count)
        self._code_size = code_size
        self._column_number = column_number

    def build(self, images: List[Image.Image]) -> Image:

        image_iter = iter(images)
        collage_canvas = Image.new('RGB', (self._collage_size.width, self._collage_size.height), (250, 250, 250))

        for row_index in range(len(images)):

            for column_index in range(self._column_number):

                try:
                    next_image = next(image_iter)

                    pos_x = self._code_size.width * column_index
                    pos_y = ImageSize.from_image(next_image).height * row_index

                    collage_canvas.paste(next_image, (pos_x, pos_y))
                except StopIteration:
                    return collage_canvas

        return collage_canvas
