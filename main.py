import random
from typing import List
import requests
from io import BytesIO

from PIL import Image
from collage_builder import AccurateCollageBuilder
from core import ImageSize
from spotify_utils import get_playlist_track_uris, create_spotify_code_url, SpotifyImageFormat, SpotifyBarColor, \
    DefaultSpotifyBackgroundColor

PLAYLIST_URI = "spotify:playlist:2VTUoPFycbGS5AjOsmXZRy"
RESULT_PATH = "result_collage.jpg"
CODE_SIZE = 256


def _get_tracks_code_urls(code_size: int, track_uri_list: List[str]) -> List[str]:
    code_url_list = []

    for track_uri in track_uri_list:
        code_color = random.choice(list(DefaultSpotifyBackgroundColor))

        code_url = create_spotify_code_url(
            spotify_uri=track_uri,
            size_px=code_size,
            image_format=SpotifyImageFormat.jpeg,
            code_color_hex=code_color.value,
            bar_color=SpotifyBarColor.white
        )
        code_url_list.append(code_url)

    return code_url_list


def _get_image_by_url(url: str) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def create_collage(path):
    track_uris = get_playlist_track_uris(PLAYLIST_URI)
    code_url_list = _get_tracks_code_urls(CODE_SIZE, track_uris)

    images = []

    for code_url in code_url_list:
        code_image = _get_image_by_url(code_url)
        images.append(code_image)

    if len(images) > 0:
        first_code_image = images[0]
        first_code_image_size = ImageSize.from_image(first_code_image)

        canvas_size = ImageSize(first_code_image.width, first_code_image_size.height * len(images))
        collage = AccurateCollageBuilder().build(canvas_size, images)

        collage.show()
        collage.save(path, "JPEG")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_collage(RESULT_PATH)
