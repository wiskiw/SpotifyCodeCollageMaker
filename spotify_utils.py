import random
from typing import List

from spotipy import SpotifyClientCredentials, Spotify
from enum import Enum


class SpotifyBarColor(Enum):
    white = "white"
    black = "black"


class SpotifyImageFormat(Enum):
    png = "png"
    jpeg = "jpeg"
    swg = "swg"


SPOTIFY_CLIENT_ID = "fill me please"
SPOTIFY_CLIENT_SECRET = "fill me please"

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
spotify = Spotify(client_credentials_manager=client_credentials_manager)


# Src : https://github.com/spotify/web-api/issues/519#issuecomment-618114678
def _create_spotify_code_url(
        spotify_uri: str,
        size_px: int,
        image_format: SpotifyImageFormat = SpotifyImageFormat.jpeg,
        bar_color: SpotifyBarColor = SpotifyBarColor.white,
        bg_color_hex: str = "000000",
) -> str:
    return f"https://scannables.scdn.co/uri/plain/{image_format.value}/{bg_color_hex}/{bar_color.value}/{size_px}/{spotify_uri}"


def get_playlist_track_uris(playlist_uri: str) -> List[str]:
    playlist = spotify.playlist(playlist_uri)
    tracks = playlist['tracks']["items"]

    uri_list = []
    for track in tracks:
        track_uri = track['track']['uri']
        uri_list.append(track_uri)

    return uri_list


def get_tracks_code_urls(code_size: int, track_uri_list: List[str]) -> List[str]:
    code_url_list = []

    for track_uri in track_uri_list:
        code_url = _create_spotify_code_url(
            spotify_uri=track_uri,
            size_px=code_size,
            image_format=SpotifyImageFormat.jpeg,
            bar_color=random.choice(list(SpotifyBarColor))
        )
        code_url_list.append(code_url)

    return code_url_list
