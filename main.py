import random
import requests
import argparse

from typing import List
from io import BytesIO
from PIL import Image

from collage_builder import ColumnCollageBuilder, CollageBuilder
from core import ImageSize, create_dir
from spotify_utils import get_playlist_track_uris, create_spotify_code_url, SpotifyImageFormat, SpotifyBarColor, \
    DefaultSpotifyBackgroundColor, DEFAULT_CODE_IMAGE_HEIGHT

RESULT_FILE_PATH = "./result/result_collage.jpg"


def _get_tracks_code_urls(image_width: int, track_uri_list: List[str]) -> List[str]:
    code_url_list = []

    for track_uri in track_uri_list:
        code_color = random.choice(list(DefaultSpotifyBackgroundColor))

        code_url = create_spotify_code_url(
            spotify_uri=track_uri,
            size=image_width,
            image_format=SpotifyImageFormat.jpeg,
            code_color_hex=code_color.value,
            bar_color=SpotifyBarColor.white
        )
        code_url_list.append(code_url)

    return code_url_list


def _get_image_by_url(url: str) -> Image.Image:
    response = requests.get(url)
    return Image.open(BytesIO(response.content))


def _load_images(image_urls: List[str]) -> List[Image.Image]:
    images = []

    for index, image_url in enumerate(image_urls):
        code_image = _get_image_by_url(image_url)
        print(f"Downloading image {index + 1}/{len(image_urls)}")
        images.append(code_image)

    print(f"All images ({len(image_urls)}) downloaded!")

    return images


def _create_collage(track_uri_list: List[str], collage_builder: CollageBuilder) -> Image.Image:
    code_image_size = builder.get_code_size()
    code_url_list = _get_tracks_code_urls(code_image_size.width, track_uri_list)
    code_images = _load_images(code_url_list)

    return collage_builder.build(code_images)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_uri", help="Spotify URI for source playlist", type=str)
    parser.add_argument('--show', help="Open final image when finished", action='store_true', default=False)

    args = parser.parse_args()

    playlist_uri = args.playlist_uri
    print(f"Launch for playlist URI:{playlist_uri}")

    track_uris = get_playlist_track_uris(playlist_uri)
    track_count = len(track_uris)

    canvas_size = ImageSize(256, DEFAULT_CODE_IMAGE_HEIGHT * track_count)
    builder = ColumnCollageBuilder(canvas_size, track_count)

    collage = _create_collage(track_uri_list=track_uris, collage_builder=builder)

    create_dir(RESULT_FILE_PATH)
    collage.save(RESULT_FILE_PATH, "JPEG")

    if args.show:
        collage.show()
