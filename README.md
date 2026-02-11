# 🎵 Spotify Playlist Creator from Billboard Hot 100

Aplikacja webowa Flask, która tworzy playlisty Spotify na podstawie list Billboard Hot 100 z wybranej daty.

## ✨ Funkcjonalności

- 📅 Wybór daty z kalendarza (od 1958-08-04 do dzisiaj)
- 🎨 Możliwość nadania własnej nazwy playliście
- 🔍 Automatyczne scrapowanie list Billboard Hot 100
- 🎶 Wyszukiwanie utworów na Spotify
- 📝 Tworzenie prywatnej playlisty na Twoim koncie Spotify
- 🔐 Bezpieczna autoryzacja przez Spotify OAuth

## 🚀 Instalacja

### 1. Sklonuj repozytorium

```bash
git clone <repository-url>
cd Playlist_Scraper_Spotify
```

### 2. Utwórz wirtualne środowisko

```bash
python -m venv .venv
```

### 3. Aktywuj środowisko

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\activate
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 4. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

## ⚙️ Konfiguracja

### 1. Utwórz aplikację Spotify

1. Przejdź do [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Zaloguj się swoim kontem Spotify
3. Kliknij **"Create app"**
4. Wypełnij formularz:
   - **App name**: Dowolna nazwa (np. "Billboard Playlist Creator")
   - **App description**: Dowolny opis
   - **Redirect URI**: `http://127.0.0.1:8080/callback`
   - **Website**: (opcjonalne)
   - **APIs used**: Zaznacz odpowiednie (Web API)
5. Zapisz aplikację
6. Skopiuj **Client ID** i **Client Secret**

### 2. Utwórz plik `.env`

Utwórz plik `.env` w głównym katalogu projektu:

```env
SPOTIPY_CLIENT_ID=twoj_client_id
SPOTIPY_CLIENT_SECRET=twoj_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8080/callback

FLASK_SECRET_KEY=losowy_sekretny_klucz
```

**Ważne:** 
- Zamień `twoj_client_id` i `twoj_client_secret` na dane z Spotify Dashboard
- `FLASK_SECRET_KEY` może być dowolnym losowym ciągiem znaków

## 🎮 Uruchomienie

```bash
python run.py
```

Aplikacja będzie dostępna pod adresem: **http://127.0.0.1:8080**

## 📖 Jak używać

1. **Otwórz aplikację** w przeglądarce (http://127.0.0.1:8080)
2. **Wybierz datę** z kalendarza
3. **(Opcjonalnie)** Wpisz własną nazwę playlisty
4. **Kliknij "Generate Playlist"**
5. **Zaloguj się** na swoje konto Spotify (jeśli jeszcze nie jesteś zalogowany)
6. **Zatwierdź uprawnienia** dla aplikacji
7. **Gotowe!** Playlista została utworzona na Twoim koncie

## 🧪 Testy

Projekt zawiera kompletny zestaw testów jednostkowych i integracyjnych.

### Uruchomienie testów

```bash
# Wszystkie testy
pytest

# Z pokryciem kodu
pytest --cov=app --cov-report=html

# Szczegółowy output
pytest -v

# Konkretny plik testów
pytest tests/test_utils.py
```

### Statystyki testów

- **Łącznie testów**: 60+
- **Pliki testowe**: 5 modułów
- **Pokrycie**: utils, scraper, spotify, routes, integration

Zobacz więcej w [`tests/README.md`](tests/README.md)

## 📁 Struktura projektu

```
Playlist_Scraper_Spotify/
├── app/
│   ├── __init__.py          # Inicjalizacja Flask
│   ├── routes.py            # Endpointy aplikacji
│   ├── scraper.py           # Scraper Billboard
│   ├── spotify.py           # Klient Spotify API
│   ├── utils.py             # Funkcje pomocnicze
│   ├── static/
│   │   └── style.css        # Style CSS
│   └── templates/
│       ├── base.html        # Szablon bazowy
│       ├── index.html       # Strona główna
│       └── playlist_created.html  # Strona sukcesu
├── tests/                   # Testy pytest
├── run.py                   # Entry point aplikacji
├── main.py                  # Standalone wersja (CLI)
├── requirements.txt         # Zależności Python
├── .env                     # Konfiguracja (nie w repozytorium!)
└── README.md               # Ten plik

```

## 🛠️ Technologie

- **Flask** - Framework webowy
- **Spotipy** - Biblioteka Spotify API
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP requests
- **python-dotenv** - Zarządzanie zmiennymi środowiskowymi
- **Pytest** - Framework testowy

## 🔒 Bezpieczeństwo

- **OAuth 2.0** - Bezpieczna autoryzacja przez Spotify
- **Brak przechowywania haseł** - Tokeny w sesji
- **Prywatne playlisty** - Domyślnie playlisty są prywatne
- **`.env` w .gitignore** - Dane wrażliwe nie trafiają do repozytorium

## ⚠️ Uwagi

- Aplikacja wymaga połączenia z internetem (Billboard i Spotify API)
- Niektóre utwory mogą nie być dostępne na Spotify
- Billboard Hot 100 istnieje od **4 sierpnia 1958 roku**
- Aplikacja jest w trybie **development** - nie używaj w produkcji bez odpowiedniej konfiguracji



