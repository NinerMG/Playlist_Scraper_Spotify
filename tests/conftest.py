"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Dodaj główny katalog do ścieżki
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app


@pytest.fixture
def app():
    """Fixture zwracający aplikację Flask"""
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret_key",
        "WTF_CSRF_ENABLED": False
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Fixture zwracający test client Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture zwracający CLI runner"""
    return app.test_cli_runner()
