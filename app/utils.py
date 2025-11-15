from datetime import datetime


def validate_date(date_str):
    """
    Sprawdza, czy data jest w formacie YYYY-MM-DD.
    Zwraca True jeśli poprawna, False jeśli niepoprawna.
    """
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def clean_song_title(title):
    """
    Czyści tytuł utworu ze zbędnych spacji i znaków nowej linii.
    """
    if not isinstance(title, str):
        return ""
    return title.strip()


def chunk_list(lst, n):
    """
    Dzieli listę na kawałki po n elementów.
    Przydatne np. przy dodawaniu utworów do playlisty po batchach.
    """
    if not isinstance(lst, list) or n <= 0:
        raise ValueError("Invalid list or chunk size")

    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def safe_int(value, default=None):
    """
    Próbuje przekonwertować wartość na int.
    Zwraca default jeśli się nie uda.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=None):
    """
    Próbuje przekonwertować wartość na float.
    Zwraca default jeśli się nie uda.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
