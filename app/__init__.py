from flask import Flask
from dotenv import load_dotenv
import os

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Inicjalizacja Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")

# Import i rejestracja Blueprint
from app.routes import routes
app.register_blueprint(routes)
