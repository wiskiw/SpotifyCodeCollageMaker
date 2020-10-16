import argparse

from PIL import Image

from collage_builder import SingleSizeColumnCollageBuilder
from color_factory import SpotifyOrderedColorFactory, SpotifyRandomColorFactory, SingleColorFactory, ColorFactory
from core import ImageSize, create_dir
from image_code_provider import PlaylistProvider
from spotify_utils import get_playlist_name, SpotifyCodeColor, DefaultSpotifyBackgroundColor, SpotifyBarColor

_RESULT_FILE_FOLDER = "./result/"
_RESULT_FILE_EXTENSION = ".png"
_DEFAULT_CODE_IMAGE_WIDTH = 256

_IMAGE_FACTORY_NAME_ORDERED = "ordered_colors"
_IMAGE_FACTORY_NAME_RANDOM = "random_colors"
_IMAGE_FACTORY_NAME_SINGLE = "single_color"


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_uri", help="Spotify URI for source playlist", type=str)
    parser.add_argument('column_count', help="Number of columns", type=int)
    parser.add_argument('--show', help="Open final image when finished", action='store_true', default=False)

    _default_size = _DEFAULT_CODE_IMAGE_WIDTH
    parser.add_argument(
        '--size',
        help=f"Size(width) of individual track code (128, 256, 512, etc). ({_default_size} default)",
        type=int,
        default=_DEFAULT_CODE_IMAGE_WIDTH
    )
    parser.add_argument('--shuffle', help="Shuffle tracks in the playlist", action='store_true', default=False)

    _default_color_factory_name = _IMAGE_FACTORY_NAME_RANDOM
    parser.add_argument(
        '--color_factory',
        dest="color_factory_name",
        help=f"Color choose strategy for individual code image ('{_default_color_factory_name}' default)",
        type=str,
        choices=[_IMAGE_FACTORY_NAME_ORDERED, _IMAGE_FACTORY_NAME_RANDOM, _IMAGE_FACTORY_NAME_SINGLE],
        default=_default_color_factory_name
    )

    _default_bar_color = SpotifyBarColor.white.value
    parser.add_argument(
        '--bar_color',
        help=f"Color of code image bars ('{_default_bar_color}' default)",
        choices=list(map(lambda it: it.value, list(SpotifyBarColor))),
        type=str,
        default=_default_bar_color
    )

    _default_bg_color_hex = DefaultSpotifyBackgroundColor.black.value
    parser.add_argument(
        '--bg_color_hex',
        help=f"Color of code image background ('{_default_bg_color_hex}' default)",
        type=str,
        default=_default_bg_color_hex
    )

    return parser.parse_args()


def _get_color_factory_by_name(factory_name: str, code_color: SpotifyCodeColor) -> ColorFactory:
    _factory_mapping = {
        _IMAGE_FACTORY_NAME_ORDERED: SpotifyOrderedColorFactory(code_color.bar),
        _IMAGE_FACTORY_NAME_RANDOM: SpotifyRandomColorFactory(code_color.bar),
        _IMAGE_FACTORY_NAME_SINGLE: SingleColorFactory(code_color)
    }

    try:
        return _factory_mapping[factory_name]
    except KeyError as e:
        raise ValueError(f"Undefined color factory name: '{factory_name}'")


def _create_collage_for_playlist(
        playlist_uri: str,
        color_factory: ColorFactory,
        column_count: int,
        code_width: int,
        shuffle: bool
) -> Image.Image:
    print(f"Fetching tracks from playlist URI:{playlist_uri}")

    code_size = ImageSize(
        width=code_width,
        height=PlaylistProvider.get_code_height(code_width)
    )

    image_provider = PlaylistProvider(code_size.width, playlist_uri, color_factory, shuffle)

    code_images = image_provider.get_code_images()
    code_count = len(code_images)

    canvas_size = ImageSize(
        width=code_size.width * column_count,
        height=code_size.height * round(code_count / column_count)
    )

    collage_builder = SingleSizeColumnCollageBuilder(canvas_size, code_size, code_count, column_count)

    return collage_builder.build(code_images)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    _args = _get_args()

    _playlist_name = get_playlist_name(_args.playlist_uri)
    print(f"Found playlist '{_playlist_name}'!")

    _bar_color = SpotifyBarColor[_args.bar_color]
    _color_factory = _get_color_factory_by_name(
        _args.color_factory_name,
        SpotifyCodeColor(bar=_bar_color, background_hex=_args.bg_color_hex)
    )

    _collage = _create_collage_for_playlist(
        playlist_uri=_args.playlist_uri,
        color_factory=_color_factory,
        column_count=_args.column_count,
        code_width=_args.size,
        shuffle=_args.shuffle
    )

    _result_path = f"{_RESULT_FILE_FOLDER}{_playlist_name}-{_args.column_count}x{_args.size}{_RESULT_FILE_EXTENSION}"
    create_dir(_result_path)
    _collage.save(_result_path, "PNG")

    if _args.show:
        _collage.show()
