"""
Testy integracyjne - testują współpracę różnych modułów
"""
import pytest
import sys
from unittest.mock import patch, MagicMock


class TestFullFlow:
    """Testy pełnego flow aplikacji"""
    
    def test_complete_workflow(self, client):
        """Test kompletnego przepływu od strony głównej do utworzenia playlisty"""
        
        # 1. Mock scrapera
        mock_scraper_result = ['Song 1', 'Song 2', 'Song 3']
        
        # 2. Mock Spotify client
        mock_spotify = MagicMock()
        mock_spotify.get_auth_url.return_value = "https://accounts.spotify.com/authorize?..."
        mock_spotify.create_playlist_from_songs.return_value = "https://open.spotify.com/playlist/abc123"
        
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'get_top_100', return_value=mock_scraper_result):
            with patch.object(routes_module, 'SpotifyClient', return_value=mock_spotify):
                # Krok 1: Odwiedź stronę główną
                response = client.get('/')
                assert response.status_code == 200
                
                # Krok 2: Wyślij formularz z datą
                response = client.post('/start', data={
                    'date': '2024-01-15',
                    'playlist_name': 'Integration Test Playlist'
                }, follow_redirects=False)
                
                assert response.status_code == 302
                assert "spotify.com" in response.location
                
                # Krok 3: Symuluj callback od Spotify
                with client.session_transaction() as sess:
                    sess['selected_date'] = '2024-01-15'
                    sess['playlist_name'] = 'Integration Test Playlist'
                
                response = client.get('/callback?code=test_auth_code', follow_redirects=False)
                assert response.status_code == 302
                
                # Krok 4: Utwórz playlistę
                response = client.get('/create_playlist', follow_redirects=True)
                assert response.status_code == 200
                
                # Sprawdź czy wszystkie funkcje zostały wywołane
                routes_module.get_top_100.assert_called_once_with('2024-01-15')
                mock_spotify.fetch_token.assert_called_once_with('test_auth_code')
                mock_spotify.create_playlist_from_songs.assert_called_once()


class TestErrorHandling:
    """Testy obsługi błędów"""
    
    def test_scraper_failure_handling(self, client):
        """Test obsługi błędu scrapera"""
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'get_top_100', side_effect=Exception("Billboard unavailable")):
            with client.session_transaction() as sess:
                sess['selected_date'] = '2024-01-15'
            
            response = client.get('/create_playlist', follow_redirects=True)
            assert response.status_code == 200
            assert b'Failed' in response.data or b'error' in response.data.lower()
    
    def test_spotify_failure_handling(self, client):
        """Test obsługi błędu Spotify"""
        mock_scraper_result = ['Song 1', 'Song 2']
        
        mock_spotify = MagicMock()
        mock_spotify.create_playlist_from_songs.side_effect = Exception("Spotify API error")
        
        routes_module = sys.modules['app.routes']
        with patch.object(routes_module, 'get_top_100', return_value=mock_scraper_result):
            with patch.object(routes_module, 'SpotifyClient', return_value=mock_spotify):
                with client.session_transaction() as sess:
                    sess['selected_date'] = '2024-01-15'
                
                response = client.get('/create_playlist', follow_redirects=True)
                assert response.status_code == 200
                assert b'failed' in response.data.lower() or b'error' in response.data.lower()


class TestSessionManagement:
    """Testy zarządzania sesją"""
    
    def test_session_persistence(self, client):
        """Test czy sesja zachowuje dane między requestami"""
        with client.session_transaction() as sess:
            sess['selected_date'] = '2024-01-15'
            sess['playlist_name'] = 'Test Playlist'
        
        with client.session_transaction() as sess:
            assert sess.get('selected_date') == '2024-01-15'
            assert sess.get('playlist_name') == 'Test Playlist'
    
    def test_missing_session_data(self, client):
        """Test reakcji na brak danych w sesji"""
        response = client.get('/create_playlist', follow_redirects=True)
        assert response.status_code == 200
        assert b'expired' in response.data.lower() or b'try again' in response.data.lower()
