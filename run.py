from app import app

# Uruchomienie aplikacji
if __name__ == "__main__":
    # Debug=True tylko do developmentu, w produkcji ustaw False
    app.run(host="127.0.0.1", port=8080, debug=True)
