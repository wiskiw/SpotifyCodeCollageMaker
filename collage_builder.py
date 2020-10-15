from typing import List
from PIL import Image
from core import ImageSize

from spotify_utils import get_code_height


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
    _column_number = 1
    _column_width = 0

    def __init__(self, collage_size: ImageSize, track_count: int, column_number: int = 1):
        super(ColumnCollageBuilder, self).__init__(collage_size, track_count)
        self._column_number = column_number
        self._column_width = round(self.collage_size.width / column_number)

    def get_code_size(self) -> ImageSize:
        return ImageSize(self._column_width, get_code_height(self._column_width))

    def build(self, images: List[Image.Image]) -> Image:

        image_iter = iter(images)
        collage_canvas = Image.new('RGB', (self.collage_size.width, self.collage_size.height), (250, 250, 250))

        for row_index in range(len(images)):

            for column_index in range(self._column_number):

                try:
                    next_image = next(image_iter)

                    pos_x = self._column_width * column_index
                    pos_y = ImageSize.from_image(next_image).height * row_index

                    collage_canvas.paste(next_image, (pos_x, pos_y))
                except StopIteration:
                    return collage_canvas

        return collage_canvas
