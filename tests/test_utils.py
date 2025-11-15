"""
Testy dla modułu utils
"""
import pytest
from app.utils import (
    validate_date,
    clean_song_title,
    chunk_list,
    safe_int,
    safe_float
)


class TestValidateDate:
    """Testy walidacji daty"""
    
    def test_valid_date(self):
        """Test poprawnej daty"""
        assert validate_date("2024-01-15") is True
        assert validate_date("1990-12-31") is True
        assert validate_date("2000-06-01") is True
    
    def test_invalid_format(self):
        """Test niepoprawnego formatu"""
        assert validate_date("15-01-2024") is False
        assert validate_date("2024/01/15") is False
        assert validate_date("01-15-2024") is False
    
    def test_invalid_date(self):
        """Test niepoprawnych dat"""
        assert validate_date("2024-13-01") is False  # miesiąc > 12
        assert validate_date("2024-02-30") is False  # luty nie ma 30 dni
        assert validate_date("2024-00-01") is False  # miesiąc 0
    
    def test_invalid_input(self):
        """Test niepoprawnych inputów"""
        assert validate_date("") is False
        assert validate_date("not-a-date") is False
        assert validate_date("2024") is False


class TestCleanSongTitle:
    """Testy czyszczenia tytułów piosenek"""
    
    def test_clean_whitespace(self):
        """Test usuwania białych znaków"""
        assert clean_song_title("  Song Title  ") == "Song Title"
        assert clean_song_title("\nSong\n") == "Song"
        assert clean_song_title("\t  Title  \t") == "Title"
    
    def test_empty_string(self):
        """Test pustego stringa"""
        assert clean_song_title("") == ""
        assert clean_song_title("   ") == ""
    
    def test_non_string_input(self):
        """Test niepoprawnego typu"""
        assert clean_song_title(None) == ""
        assert clean_song_title(123) == ""
        assert clean_song_title([]) == ""


class TestChunkList:
    """Testy dzielenia listy na kawałki"""
    
    def test_basic_chunking(self):
        """Test podstawowego dzielenia"""
        result = list(chunk_list([1, 2, 3, 4, 5], 2))
        assert result == [[1, 2], [3, 4], [5]]
    
    def test_exact_chunks(self):
        """Test gdy lista dzieli się równo"""
        result = list(chunk_list([1, 2, 3, 4], 2))
        assert result == [[1, 2], [3, 4]]
    
    def test_chunk_larger_than_list(self):
        """Test gdy chunk większy niż lista"""
        result = list(chunk_list([1, 2], 5))
        assert result == [[1, 2]]
    
    def test_invalid_input(self):
        """Test niepoprawnych argumentów"""
        with pytest.raises(ValueError):
            list(chunk_list("not a list", 2))
        
        with pytest.raises(ValueError):
            list(chunk_list([1, 2, 3], 0))
        
        with pytest.raises(ValueError):
            list(chunk_list([1, 2, 3], -1))


class TestSafeInt:
    """Testy bezpiecznej konwersji na int"""
    
    def test_valid_conversion(self):
        """Test poprawnej konwersji"""
        assert safe_int("123") == 123
        assert safe_int(456) == 456
        assert safe_int("0") == 0
        assert safe_int(-10) == -10
    
    def test_invalid_conversion(self):
        """Test niepoprawnej konwersji"""
        assert safe_int("abc") is None
        assert safe_int("12.34") is None
        assert safe_int(None) is None
        assert safe_int([]) is None
    
    def test_custom_default(self):
        """Test własnej wartości domyślnej"""
        assert safe_int("abc", default=0) == 0
        assert safe_int(None, default=-1) == -1


class TestSafeFloat:
    """Testy bezpiecznej konwersji na float"""
    
    def test_valid_conversion(self):
        """Test poprawnej konwersji"""
        assert safe_float("12.34") == 12.34
        assert safe_float(45.67) == 45.67
        assert safe_float("0") == 0.0
        assert safe_float(10) == 10.0
    
    def test_invalid_conversion(self):
        """Test niepoprawnej konwersji"""
        assert safe_float("abc") is None
        assert safe_float(None) is None
        assert safe_float([]) is None
    
    def test_custom_default(self):
        """Test własnej wartości domyślnej"""
        assert safe_float("abc", default=0.0) == 0.0
        assert safe_float(None, default=-1.5) == -1.5
