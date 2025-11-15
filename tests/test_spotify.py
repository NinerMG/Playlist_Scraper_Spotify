"""
Testy dla modułu spotify
"""
import pytest
from unittest.mock import patch, MagicMock
from app.spotify import SpotifyClient


class TestSpotifyClient:
    """Testy dla klasy SpotifyClient"""
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    def test_init(self):
        """Test inicjalizacji klienta"""
        client = SpotifyClient()
        
        assert client.client_id == 'test_id'
        assert client.client_secret == 'test_secret'
        assert client.redirect_uri == 'http://localhost:8080/callback'
        assert client.scope == "playlist-modify-public playlist-modify-private"
        assert client.sp is None
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    @patch('app.spotify.SpotifyOAuth')
    def test_get_auth_url(self, mock_oauth):
        """Test generowania URL autoryzacji"""
        # Mock OAuth
        mock_oauth_instance = MagicMock()
        mock_oauth_instance.get_authorize_url.return_value = "https://spotify.com/auth"
        mock_oauth_instance.state = "random_state"
        mock_oauth.return_value = mock_oauth_instance
        
        client = SpotifyClient()
        
        with patch('app.spotify.session', {}) as mock_session:
            auth_url = client.get_auth_url()
        
        assert auth_url == "https://spotify.com/auth"
        mock_oauth.assert_called_once_with(
            client_id='test_id',
            client_secret='test_secret',
            redirect_uri='http://localhost:8080/callback',
            scope="playlist-modify-public playlist-modify-private",
            show_dialog=True,
            cache_path=None
        )
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    @patch('app.spotify.spotipy.Spotify')
    @patch('app.spotify.SpotifyOAuth')
    def test_fetch_token(self, mock_oauth, mock_spotify):
        """Test pobierania tokenu"""
        # Mock OAuth
        mock_oauth_instance = MagicMock()
        mock_oauth_instance.get_access_token.return_value = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh'
        }
        mock_oauth.return_value = mock_oauth_instance
        
        client = SpotifyClient()
        
        with patch('app.spotify.session', {}) as mock_session:
            client.fetch_token('test_code')
        
        mock_oauth_instance.get_access_token.assert_called_once_with('test_code')
        mock_spotify.assert_called_once_with(auth='test_token')
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    def test_search_song_found(self):
        """Test wyszukiwania piosenki - znaleziona"""
        client = SpotifyClient()
        
        # Mock spotipy client
        mock_sp = MagicMock()
        mock_sp.search.return_value = {
            'tracks': {
                'items': [
                    {'uri': 'spotify:track:123abc'}
                ]
            }
        }
        client.sp = mock_sp
        
        uri = client.search_song("Test Song", "2024")
        
        assert uri == 'spotify:track:123abc'
        mock_sp.search.assert_called_once_with(
            q='track:Test Song year:2024',
            type='track'
        )
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    def test_search_song_not_found(self):
        """Test wyszukiwania piosenki - nie znaleziona"""
        client = SpotifyClient()
        
        # Mock spotipy client
        mock_sp = MagicMock()
        mock_sp.search.return_value = {
            'tracks': {
                'items': []
            }
        }
        client.sp = mock_sp
        
        uri = client.search_song("Nonexistent Song", "2024")
        
        assert uri is None
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    def test_create_playlist_with_custom_name(self):
        """Test tworzenia playlisty z własną nazwą"""
        client = SpotifyClient()
        
        # Mock spotipy client
        mock_sp = MagicMock()
        mock_sp.current_user.return_value = {'id': 'user123'}
        mock_sp.search.return_value = {
            'tracks': {
                'items': [{'uri': 'spotify:track:abc'}]
            }
        }
        mock_sp.user_playlist_create.return_value = {
            'id': 'playlist123',
            'external_urls': {'spotify': 'https://spotify.com/playlist/123'}
        }
        client.sp = mock_sp
        
        playlist_url = client.create_playlist_from_songs(
            "2024-01-15",
            ["Song 1", "Song 2"],
            custom_name="My Custom Playlist"
        )
        
        assert playlist_url == 'https://spotify.com/playlist/123'
        
        # Sprawdź czy użyto własnej nazwy
        create_call = mock_sp.user_playlist_create.call_args
        assert create_call[1]['name'] == "My Custom Playlist"
    
    @patch.dict('os.environ', {
        'SPOTIPY_CLIENT_ID': 'test_id',
        'SPOTIPY_CLIENT_SECRET': 'test_secret',
        'SPOTIPY_REDIRECT_URI': 'http://localhost:8080/callback'
    })
    def test_create_playlist_default_name(self):
        """Test tworzenia playlisty z domyślną nazwą"""
        client = SpotifyClient()
        
        # Mock spotipy client
        mock_sp = MagicMock()
        mock_sp.current_user.return_value = {'id': 'user123'}
        mock_sp.search.return_value = {
            'tracks': {
                'items': [{'uri': 'spotify:track:abc'}]
            }
        }
        mock_sp.user_playlist_create.return_value = {
            'id': 'playlist123',
            'external_urls': {'spotify': 'https://spotify.com/playlist/123'}
        }
        client.sp = mock_sp
        
        playlist_url = client.create_playlist_from_songs(
            "2024-01-15",
            ["Song 1"]
        )
        
        # Sprawdź czy użyto domyślnej nazwy
        create_call = mock_sp.user_playlist_create.call_args
        assert create_call[1]['name'] == "2024-01-15 Billboard 100"
