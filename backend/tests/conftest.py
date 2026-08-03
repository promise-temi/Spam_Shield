import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault("BACKEND_API_KEY", "cle-de-test-1234")
os.environ.setdefault("ENCRYPTION_KEY", "RxdMLSRTwGMYW6gNoAEvlWbdOHI6iDzjssyXCMMzq2I=")

from api import app, require_api_key


@pytest.fixture
def client():
    """Client de test avec l'authentification neutralisée : les routes se comportent
    comme si une clé valide avait été fournie, sans dépendre de la vraie valeur en mémoire."""
    app.dependency_overrides[require_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_sans_override():
    """Client de test SANS neutraliser l'authentification, pour tester le mécanisme
    d'authentification lui-même (401/422)."""
    return TestClient(app)