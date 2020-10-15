import random

from spotify_utils import SpotifyCodeColor, SpotifyBarColor, DefaultSpotifyBackgroundColor


class ColorFactory:

    def get_color(self, code_index: int, codes_count: int) -> SpotifyCodeColor:
        pass


class SpotifyRandomColorFactory(ColorFactory):
    _bar_color: SpotifyBarColor

    def __init__(self, bar_color: SpotifyBarColor):
        self._bar_color = bar_color

    def get_color(self, code_index: int, codes_count: int) -> SpotifyCodeColor:
        bg_color = random.choice(list(DefaultSpotifyBackgroundColor))

        return SpotifyCodeColor(bar=self._bar_color, background_hex=bg_color.value)
        pass


class SpotifyOrderedColorFactory(ColorFactory):
    _bar_color: SpotifyBarColor

    def __init__(self, bar_color: SpotifyBarColor):
        self._bar_color = bar_color

    def get_color(self, code_index: int, codes_count: int) -> SpotifyCodeColor:
        default_colors_count = len(list(DefaultSpotifyBackgroundColor))

        color_index = code_index % default_colors_count
        bg_color = list(DefaultSpotifyBackgroundColor)[color_index]

        return SpotifyCodeColor(bar=self._bar_color, background_hex=bg_color.value)
        pass
