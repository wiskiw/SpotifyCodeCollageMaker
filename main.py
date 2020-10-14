import requests
from io import BytesIO

from PIL import Image
from collage_builder import AccurateCollageBuilder
from core import ImageSize
from spotify_utils import get_playlist_track_uris, get_tracks_code_urls

PLAYLIST_URI = "spotify:playlist:2cDXX4DJjkfoIWdHtO9Wii"
CODE_SIZE = 256


def _get_image_by_url(url: str) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def main():
    track_uris = get_playlist_track_uris(PLAYLIST_URI)
    code_url_list = get_tracks_code_urls(CODE_SIZE, track_uris)

    images = []

    for code_url in code_url_list:
        code_image = _get_image_by_url(code_url)
        images.append(code_image)

    if len(images) > 0:
        first_code_image = images[0]
        first_code_image_size = ImageSize.from_image(first_code_image)

        canvas_size = ImageSize(first_code_image.width, first_code_image_size.height * 3)
        collage = AccurateCollageBuilder().build(canvas_size, images)

        collage.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
