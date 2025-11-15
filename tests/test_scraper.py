"""
Testy dla modułu scraper
"""
import pytest
from unittest.mock import patch, MagicMock
import requests
from app.scraper import get_top_100


class TestGetTop100:
    """Testy dla funkcji get_top_100"""
    
    @patch('app.scraper.requests.get')
    def test_successful_scrape(self, mock_get):
        """Test pomyślnego scrapowania"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <li><ul><li><h3>Song 1</h3></li></ul></li>
            <li><ul><li><h3>Song 2</h3></li></ul></li>
            <li><ul><li><h3>Song 3</h3></li></ul></li>
        </html>
        '''
        mock_get.return_value = mock_response
        
        result = get_top_100("2024-01-15")
        
        assert len(result) == 3
        assert "Song 1" in result
        assert "Song 2" in result
        assert "Song 3" in result
        
        # Sprawdź czy wywołano z poprawnymi parametrami
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert "2024-01-15" in call_args[0][0]
    
    @patch('app.scraper.requests.get')
    def test_network_error(self, mock_get):
        """Test błędu sieciowego"""
        mock_get.side_effect = requests.RequestException("Network error")
        
        with pytest.raises(Exception) as exc_info:
            get_top_100("2024-01-15")
        
        assert "Error fetching Billboard page" in str(exc_info.value)
    
    @patch('app.scraper.requests.get')
    def test_http_error(self, mock_get):
        """Test błędu HTTP"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            get_top_100("2024-01-15")
        
        assert "Error fetching Billboard page" in str(exc_info.value)
    
    @patch('app.scraper.requests.get')
    def test_no_songs_found(self, mock_get):
        """Test gdy nie znaleziono piosenek"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><body>No songs here</body></html>'
        mock_get.return_value = mock_response
        
        with pytest.raises(Exception) as exc_info:
            get_top_100("2024-01-15")
        
        assert "Could not parse" in str(exc_info.value)
    
    @patch('app.scraper.requests.get')
    def test_strips_whitespace(self, mock_get):
        """Test czy usuwa białe znaki z tytułów"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '''
        <html>
            <li><ul><li><h3>  Song With Spaces  </h3></li></ul></li>
            <li><ul><li><h3>
                Multiline
                Song
            </h3></li></ul></li>
        </html>
        '''
        mock_get.return_value = mock_response
        
        result = get_top_100("2024-01-15")
        
        assert len(result) == 2
        assert result[0] == "Song With Spaces"
        assert result[1] == "Multiline Song"
    
    @patch('app.scraper.requests.get')
    def test_timeout_parameter(self, mock_get):
        """Test czy używa timeoutu"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><li><ul><li><h3>Song</h3></li></ul></li></html>'
        mock_get.return_value = mock_response
        
        get_top_100("2024-01-15")
        
        # Sprawdź czy timeout został użyty
        call_kwargs = mock_get.call_args[1]
        assert 'timeout' in call_kwargs
        assert call_kwargs['timeout'] == 10
