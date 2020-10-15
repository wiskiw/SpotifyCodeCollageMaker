import argparse

from PIL import Image

from collage_builder import SingleSizeColumnCollageBuilder
from color_factory import SpotifyOrderedColorFactory, SpotifyRandomColorFactory, SingleColorFactory
from core import ImageSize, create_dir
from image_code_provider import PlaylistProvider
from spotify_utils import get_playlist_name, SpotifyCodeColor, DefaultSpotifyBackgroundColor, SpotifyBarColor

_RESULT_FILE_PATH = "./result/collage.jpg"
_RESULT_FILE_FOLDER = "./result/"
_RESULT_FILE_EXTENSION = ".png"
_DEFAULT_CODE_IMAGE_WIDTH = 256


def _create_collage_for_playlist(playlist_uri: str, column_count: int, code_width: int) -> Image.Image:
    print(f"Fetching traks from playlist URI:{playlist_uri}")

    code_size = ImageSize(
        width=code_width,
        height=PlaylistProvider.get_code_height(code_width)
    )

    # color_factory = SpotifyRandomColorFactory(bar_color=SpotifyBarColor.white)
    color_factory = SingleColorFactory(
        SpotifyCodeColor(bar=SpotifyBarColor.white, background_hex=DefaultSpotifyBackgroundColor.black.value)
    )
    image_provider = PlaylistProvider(code_size.width, playlist_uri, color_factory)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_uri", help="Spotify URI for source playlist", type=str)
    parser.add_argument('column_count', help="Number of columns", type=int)
    parser.add_argument('--show', help="Open final image when finished", action='store_true', default=False)
    parser.add_argument(
        '--size',
        help="Size(width) of individual track code (128, 256, 512, etc)",
        type=int,
        default=_DEFAULT_CODE_IMAGE_WIDTH
    )

    args = parser.parse_args()

    playlist_name = get_playlist_name(args.playlist_uri)
    print(f"Found playlist '{playlist_name}'!")

    collage = _create_collage_for_playlist(
        playlist_uri=args.playlist_uri,
        column_count=args.column_count,
        code_width=args.size
    )

    result_path = f"{_RESULT_FILE_FOLDER}{playlist_name}-{args.column_count}x{args.size}{_RESULT_FILE_EXTENSION}"
    create_dir(result_path)
    collage.save(result_path, "PNG")

    if args.show:
        collage.show()
