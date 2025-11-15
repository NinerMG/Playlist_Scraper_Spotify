import requests
from bs4 import BeautifulSoup

BASIC_URL = "https://www.billboard.com/charts/hot-100/"

def get_top_100(date_str):
    """
    Pobiera listę top 100 utworów z Billboard dla podanej daty (YYYY-MM-DD)
    Zwraca listę nazw utworów.
    """
    url = BASIC_URL + date_str
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Error fetching Billboard page: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Selekcja tytułów utworów
    song_spans = soup.select("li ul li h3")
    if not song_spans:
        raise Exception("Could not parse Billboard page — selector may have changed.")

    # Normalizuj białe znaki (zamień wiele białych znaków na jedną spację)
    songs = [" ".join(song.get_text().split()) for song in song_spans]
    return songs
