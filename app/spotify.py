import os
from flask import session, url_for
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class SpotifyClient:
    def __init__(self):
        self.client_id = os.environ.get("SPOTIPY_CLIENT_ID")
        self.client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri = os.environ.get("SPOTIPY_REDIRECT_URI")
        self.scope = "playlist-modify-public playlist-modify-private"
        self.sp = None

    def get_auth_url(self):
        """
                Tworzy URL do logowania użytkownika Spotify.
                """
        oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            show_dialog=True,
            cache_path=None  # Wyłączamy cache, który może powodować problemy
        )
        auth_url = oauth.get_authorize_url()

        session["oauth_state"] = oauth.state
        return auth_url

    def fetch_token(self, code):
        """
        Wymienia code od Spotify na access token i zapisuje w sesji.
        """
        oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_path=None  # Wyłączamy cache
        )
        token_info = oauth.get_access_token(code)
        session["spotify_token"] = token_info
        # Tworzymy obiekt spotipy do dalszego użycia
        self.sp = spotipy.Spotify(auth=token_info["access_token"])

    def get_user_id(self):
        """
        Zwraca Spotify user_id aktualnie zalogowanego użytkownika.
        """
        if not self.sp:
            token_info = session.get("spotify_token")
            if not token_info:
                raise Exception("User is not authenticated.")
            self.sp = spotipy.Spotify(auth=token_info["access_token"])
        return self.sp.current_user()["id"]

    def search_song(self, song_name, year):
        """
        Szuka utworu na Spotify, zwraca URI pierwszego trafienia.
        """
        if not self.sp:
            token_info = session.get("spotify_token")
            if not token_info:
                raise Exception("User is not authenticated.")
            self.sp = spotipy.Spotify(auth=token_info["access_token"])

        result = self.sp.search(q=f"track:{song_name} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            return uri
        except IndexError:
            return None

    def create_playlist_from_songs(self, date_str, song_list, custom_name=None):
        """
        Tworzy playlistę na koncie zalogowanego użytkownika.
        Zwraca link do playlisty.
        """
        user_id = self.get_user_id()
        year = date_str.split("-")[0]

        # Tworzymy URI dla piosenek
        song_uris = []
        for song in song_list:
            uri = self.search_song(song, year)
            if uri:
                song_uris.append(uri)

        # Ustaw nazwę playlisty
        playlist_name = custom_name if custom_name else f"{date_str} Billboard 100"

        # Tworzymy playlistę
        playlist = self.sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False,
            description=f"Top songs from {date_str}"
        )
        # Dodajemy utwory
        if song_uris:
            self.sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

        return playlist["external_urls"]["spotify"]