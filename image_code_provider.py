import random
from typing import List

from PIL import Image

from color_factory import ColorFactory
from core import get_image_by_url
from spotify_utils import get_playlist_track_uris, create_spotify_code_url, SpotifyImageFormat


class ImageProvider:

    def get_code_images(self) -> List[Image.Image]:
        pass


class PlaylistProvider(ImageProvider):
    _CODE_WIDTH_TO_HEIGHT_ASPECT_RATION = 1 / 4
    _IMAGE_CODE_FORMAT = SpotifyImageFormat.png

    @staticmethod
    def get_code_height(code_width) -> int:
        return round(code_width * PlaylistProvider._CODE_WIDTH_TO_HEIGHT_ASPECT_RATION)

    @staticmethod
    def _load_images(image_urls: List[str]) -> List[Image.Image]:
        images = []

        for index, image_url in enumerate(image_urls):
            print(f"Downloading image {index + 1}/{len(image_urls)}: {image_url}")
            code_image = get_image_by_url(image_url)
            images.append(code_image)

        print(f"All images ({len(image_urls)}) downloaded!")

        return images

    _image_width: int
    _track_uris: List[str]
    _color_factory: ColorFactory
    _shuffle: bool

    def __init__(self, image_width: int, playlist_uri: str, color_factory: ColorFactory, shuffle: bool = False):
        self._image_width = image_width
        self._track_uris = get_playlist_track_uris(playlist_uri)
        self._color_factory = color_factory
        self._shuffle = shuffle

    def _get_tracks_code_urls(self) -> List[str]:
        codes_count = len(self._track_uris)
        code_url_list = []

        for track_index, track_uri in enumerate(self._track_uris):
            spotify_track_code_color = self._color_factory.get_color(track_index, codes_count)

            code_url = create_spotify_code_url(
                spotify_uri=track_uri,
                size=self._image_width,
                image_format=PlaylistProvider._IMAGE_CODE_FORMAT,
                bg_color_hex=spotify_track_code_color.background_hex,
                bar_color=spotify_track_code_color.bar
            )
            code_url_list.append(code_url)

        return code_url_list

    def get_code_images(self) -> List[Image.Image]:
        code_url_list = self._get_tracks_code_urls()

        if self._shuffle:
            random.shuffle(code_url_list)

        return self._load_images(code_url_list)
