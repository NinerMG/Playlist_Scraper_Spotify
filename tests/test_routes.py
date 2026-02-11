"""
Testy dla routes (endpointy Flask)
"""
import pytest
import sys
from unittest.mock import patch, MagicMock


class TestIndexRoute:
    """Testy dla strony głównej"""
    
    def test_index_get(self, client):
        """Test GET na stronie głównej"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Select a date' in response.data or b'Enter a date' in response.data
    
    def test_index_contains_form(self, client):
        """Test czy strona zawiera formularz"""
        response = client.get('/')
        assert b'<form' in response.data
        assert b'date' in response.data


class TestStartRoute:
    """Testy dla endpointu /start"""
    
    def test_start_valid_date(self, client):
        """Test z poprawną datą"""
        # Mock Spotify
        mock_spotify = MagicMock()
        mock_spotify.get_auth_url.return_value = "https://spotify.com/auth"
        
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'SpotifyClient', return_value=mock_spotify):
            with client.session_transaction() as sess:
                sess['_fresh'] = True
            
            response = client.post('/start', data={
                'date': '2024-01-15',
                'playlist_name': 'Test Playlist'
            }, follow_redirects=False)
            
            assert response.status_code == 302  # redirect
            assert response.location == "https://spotify.com/auth"
    
    def test_start_invalid_date(self, client):
        """Test z niepoprawną datą"""
        response = client.post('/start', data={
            'date': 'invalid-date'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Invalid date' in response.data or b'error' in response.data.lower()
    
    def test_start_missing_date(self, client):
        """Test bez daty"""
        response = client.post('/start', data={}, follow_redirects=True)
        assert response.status_code in [200, 400]


class TestCallbackRoute:
    """Testy dla endpointu /callback"""
    
    def test_callback_with_code(self, client):
        """Test callback z kodem autoryzacyjnym"""
        mock_spotify = MagicMock()
        
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'SpotifyClient', return_value=mock_spotify):
            with client.session_transaction() as sess:
                sess['selected_date'] = '2024-01-15'
            
            response = client.get('/callback?code=test_code', follow_redirects=False)
            
            assert response.status_code == 302  # redirect
            mock_spotify.fetch_token.assert_called_once_with('test_code')
    
    def test_callback_without_code(self, client):
        """Test callback bez kodu"""
        response = client.get('/callback', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'error' in response.data.lower() or b'Authorization' in response.data


class TestCreatePlaylistRoute:
    """Testy dla endpointu /create_playlist"""
    
    def test_create_playlist_no_session(self, client):
        """Test bez daty w sesji"""
        response = client.get('/create_playlist', follow_redirects=True)
        
        assert response.status_code == 200
        assert b'expired' in response.data.lower() or b'error' in response.data.lower()
    
    def test_create_playlist_success(self, client):
        """Test pomyślnego utworzenia playlisty"""
        # Mock scraper
        mock_scraper_result = ['Song 1', 'Song 2', 'Song 3']
        
        # Mock Spotify
        mock_spotify = MagicMock()
        mock_spotify.create_playlist_from_songs.return_value = 'https://spotify.com/playlist/123'
        
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'get_top_100', return_value=mock_scraper_result):
            with patch.object(routes_module, 'SpotifyClient', return_value=mock_spotify):
                with client.session_transaction() as sess:
                    sess['selected_date'] = '2024-01-15'
                    sess['playlist_name'] = 'Test'
                    sess['spotify_token'] = {'access_token': 'test_token'}
                
                response = client.get('/create_playlist', follow_redirects=True)
                
                assert response.status_code == 200
                routes_module.get_top_100.assert_called_once_with('2024-01-15')
    
    def test_create_playlist_scraper_error(self, client):
        """Test błędu scrapera"""
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'get_top_100', side_effect=Exception("Scraper error")):
            with client.session_transaction() as sess:
                sess['selected_date'] = '2024-01-15'
            
            response = client.get('/create_playlist', follow_redirects=True)
            
            assert response.status_code == 200
            assert b'Failed' in response.data or b'error' in response.data.lower()
