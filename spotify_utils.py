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
    wtf = "AD93BF"
    pig_pink = "EA7898"
    barbie_pink = "E640A2"
    purple = "A12E8C"
    dark_purple = "50364E"


client_credentials_manager = SpotifyClientCredentials(client_id=secrets.SPOTIFY_CLIENT_ID,
                                                      client_secret=secrets.SPOTIFY_CLIENT_SECRET)
spotify = Spotify(client_credentials_manager=client_credentials_manager)


# Src : https://github.com/spotify/web-api/issues/519#issuecomment-618114678
def create_spotify_code_url(
        spotify_uri: str,
        size_px: int,
        image_format: SpotifyImageFormat = SpotifyImageFormat.jpeg,
        bar_color: SpotifyBarColor = SpotifyBarColor.white,
        code_color_hex: str = "000000",
) -> str:
    return f"https://scannables.scdn.co/uri/plain/{image_format.value}/{code_color_hex}/{bar_color.value}/{size_px}/{spotify_uri}"


def get_playlist_track_uris(playlist_uri: str) -> List[str]:
    playlist = spotify.playlist(playlist_uri)
    tracks = playlist['tracks']["items"]

    uri_list = []
    for track in tracks:
        track_uri = track['track']['uri']
        uri_list.append(track_uri)

    return uri_list
