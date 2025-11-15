# Spotify Playlist Creator - Test Suite

## Utworzone testy

### 1. `test_utils.py` - Testy funkcji pomocniczych
- ✅ Walidacja daty (formaty, niepoprawne daty)
- ✅ Czyszczenie tytułów piosenek
- ✅ Dzielenie list na chunki
- ✅ Bezpieczna konwersja na int/float

### 2. `test_scraper.py` - Testy scrapera Billboard
- ✅ Pomyślne scrapowanie danych
- ✅ Obsługa błędów sieciowych
- ✅ Obsługa błędów HTTP
- ✅ Brak znalezionych piosenek
- ✅ Czyszczenie białych znaków z tytułów
- ✅ Timeout żądań

### 3. `test_spotify.py` - Testy klienta Spotify
- ✅ Inicjalizacja klienta
- ✅ Generowanie URL autoryzacji
- ✅ Pobieranie tokenu
- ✅ Wyszukiwanie piosenek (znalezione/nieznalezione)
- ✅ Tworzenie playlisty z własną nazwą
- ✅ Tworzenie playlisty z domyślną nazwą

### 4. `test_routes.py` - Testy endpointów Flask
- ✅ Strona główna (GET)
- ✅ Endpoint /start (poprawna/niepoprawna data)
- ✅ Endpoint /callback (z kodem/bez kodu)
- ✅ Endpoint /create_playlist (sukces/błędy)

### 5. `test_integration.py` - Testy integracyjne
- ✅ Kompletny workflow aplikacji
- ✅ Obsługa błędów scrapera
- ✅ Obsługa błędów Spotify
- ✅ Zarządzanie sesją

## Uruchomienie testów

```powershell
# Zainstaluj pytest (jeśli jeszcze nie masz)
pip install pytest pytest-cov

# Uruchom wszystkie testy
pytest

# Uruchom z coverage
pytest --cov=app --cov-report=html

# Uruchom konkretny plik
pytest tests/test_utils.py

# Uruchom z więcej szczegółów
pytest -v

# Uruchom tylko szybkie testy (bez integracyjnych)
pytest -m "not slow"
```

## Statystyki

- **Łącznie testów**: ~60+
- **Pokrycie modułów**: utils, scraper, spotify, routes
- **Typy testów**: Unit, Integration, Routes
