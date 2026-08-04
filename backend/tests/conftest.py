import os
import sys
import json
import pytest
from unittest.mock import mock_open
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


# ---------- Configuration métier simulée ----------

FAKE_REQUIRED_METADATA = {
    "name": False,
    "surname": False,
    "email": False,
    "phone": False,
    "subject": False,
    "gibberish": False,
}


@pytest.fixture(autouse=True)
def mock_required_metadata_json(monkeypatch):
    """Simule le fichier required_metadata.json pour tous les tests, sans dépendre
    de sa présence réelle sur le disque (ni en local, ni dans le dépôt Git, ni en CI).

    Seuls les appels ciblant ce fichier précis sont interceptés : tout autre appel à
    open() passe normalement, pour ne pas casser d'autres lectures de fichiers.
    """
    real_open = open

    def fake_open(file, *args, **kwargs):
        if str(file).endswith("required_metadata.json"):
            return mock_open(read_data=json.dumps(FAKE_REQUIRED_METADATA))(file, *args, **kwargs)
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)