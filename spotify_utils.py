from typing import List
from spotipy import SpotifyClientCredentials, Spotify
from enum import Enum
import secrets


class SpotifyBarColor(Enum):
    white = "white"
    black = "black"


class SpotifyImageFormat(Enum):
    png = "png"
    jpeg = "jpeg"
    swg = "swg"


class DefaultSpotifyBackgroundColor(Enum):
    black = "000000"
    light_blue1 = "5394E7"
    violet = "4430E9"
    blue = "2E49AE"
    dark_blue = "1E3361"
    really_light_blue = "97BAC9"
    mint = "94E6D7"
    green = "6BDC88"
    lime = "74EC5B"
    sad_green = "4D887B"
    dark_green = "2C644F"
    sad_light_green = "BBE5C0"
    light_green = "C4EB6C"
    light_orange = "F4BE6C"
    yellow = "F1DE59"
    orange = "E99045"
    brown = "7B4937"
    light_brown = "B78D84"
    normal_brown = "BA7E5A"
    coral = "E9623D"
    light_red = "E64336"
    red = "E13139"
    dark_red = "801B33"
    pink = "F5C3C9"
    light_purple = "AD93BF"
    pig_pink = "EA7898"
    barbie_pink = "E640A2"
    purple = "A12E8C"
    dark_purple = "50364E"


class SpotifyCodeColor:
    bar: SpotifyBarColor
    background_hex: str

    def __init__(self, bar: SpotifyBarColor, background_hex: str):
        self.bar = bar
        self.background_hex = background_hex


_PLAYLIST_TRACKS_LIMIT = 100

client_credentials_manager = SpotifyClientCredentials(
    client_id=secrets.SPOTIFY_CLIENT_ID,
    client_secret=secrets.SPOTIFY_CLIENT_SECRET
)
spotify = Spotify(client_credentials_manager=client_credentials_manager)


# Src : https://github.com/spotify/web-api/issues/519#issuecomment-618114678
def create_spotify_code_url(
        spotify_uri: str,
        size: int,
        image_format: SpotifyImageFormat = SpotifyImageFormat.jpeg,
        bar_color: SpotifyBarColor = SpotifyBarColor.white,
        bg_color_hex: str = DefaultSpotifyBackgroundColor.black,
) -> str:
    return f"https://scannables.scdn.co/uri/plain/{image_format.value}/{bg_color_hex}/{bar_color.value}/{size}/{spotify_uri}"


def get_playlist_name(playlist_uri: str) -> str:
    tracks_meta = spotify.playlist(playlist_uri)
    return tracks_meta['name']


def _get_track_uti(track) -> str:
    return track['track']['uri']


def get_playlist_track_uris(playlist_uri: str) -> List[str]:
    tracks_meta = spotify.playlist_items(playlist_uri, additional_types=('track',))

    track_list = tracks_meta["items"]
    while tracks_meta['next'] is not None:
        tracks_meta = spotify.next(tracks_meta)
        track_list.extend(tracks_meta['items'])

    return list(map(_get_track_uti, track_list))
