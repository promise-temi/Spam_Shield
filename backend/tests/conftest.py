import os
import sys
import json
import pytest

from unittest.mock import mock_open
from fastapi.testclient import TestClient
from unittest.mock import patch



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.SpamShield_Operations import SpamShield_Operations
from modules.Model import Model
from modules.Metadata_Business_Rules import Metadata_Business_Rules
from modules.Database import Postgres_DB


# Fixture pour initialiser le model et faire en sorteque toutes ses dépendances aille au bon endroit
@pytest.fixture
def test_model():
    model = Model()
    model.corpus_path = "backend/tests/test_ressources/corpus.parquet"
    model.artifact_path = "backend/tests/test_ressources"
    return model

@pytest.fixture
def test_metadata_path():
    mbr = Metadata_Business_Rules("backend/tests/test_ressources/required_metadata.json")
    
    return mbr

@pytest.fixture
def test_model_pred():
    metadata = {
        'name': 'Jane',
        'surname': 'Doe',
        'email': 'Jane.Doe@email.com',
        'phone': '0605678978',
        'subject':'Ceci est un test',
        'form_id':'test'
    }
    model = Model(prediction_pipe=True, metadata=metadata)

    model.corpus_path = "backend/tests/test_ressources/corpus.parquet"
    model.artifact_path = "backend/tests/test_ressources"
    return model

# conftest.py

import pytest

@pytest.fixture
def test_db():
    db = Postgres_DB(sql_file_path="backend/modules/data/db.sql" ,prod=False)
    return db

    

# Prometheus
@pytest.fixture
def mock_monitor():
    with patch("modules.SpamShield_Operations.monitor") as mock:
        yield mock


# Ce qui est utilisé dans Preprocessing.py
@pytest.fixture
def mock_preprocessing_mlflow():
    with patch("modules.Preprocessing.ML_Flow_Operations") as mock:
        yield mock


# Ce qui est utilisé dans Model.py
@pytest.fixture
def mock_model_mlflow():
    with patch("modules.Model.ML_Flow_Operations") as mock:
        yield mock


# start_run appelé dans Model.py
@pytest.fixture
def mock_mlflow_run():
    with patch("modules.Model.mlflow.start_run"):
        yield


# Application
@pytest.fixture
def spamshield(test_db, monkeypatch):

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    return SpamShield_Operations()

# os.environ.setdefault("BACKEND_API_KEY", "cle-de-test-1234")
# os.environ.setdefault("ENCRYPTION_KEY", "RxdMLSRTwGMYW6gNoAEvlWbdOHI6iDzjssyXCMMzq2I=")
# os.environ.setdefault("MISTRAL_API_KEY", "cle-mistral-factice-pour-les-tests")

# from modapi import app, require_api_key

# TEST_RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "test_ressources")


# @pytest.fixture
# def client():
#     app.dependency_overrides[require_api_key] = lambda: None
#     yield TestClient(app)
#     app.dependency_overrides.clear()


# @pytest.fixture
# def client_sans_override():
#     return TestClient(app)


# # ---------- Configuration métier simulée (fichiers texte) ----------

# FAKE_REQUIRED_METADATA = {
#     "name": False, "surname": False, "email": False,
#     "phone": False, "subject": False, "gibberish": False,
# }
# FAKE_SYSTEM_PROMPT = "Tu es SpamShield Advisor. Prompt système factice utilisé uniquement pendant les tests."


# @pytest.fixture(autouse=True)
# def mock_fichiers_de_configuration(monkeypatch):
#     """Simule les fichiers texte de configuration (JSON, prompt système du LLM),
#     sans dépendre de leur présence réelle sur le disque."""
#     real_open = open

#     def fake_open(file, *args, **kwargs):
#         if str(file).endswith("required_metadata.json"):
#             return mock_open(read_data=json.dumps(FAKE_REQUIRED_METADATA))(file, *args, **kwargs)
#         return real_open(file, *args, **kwargs)

#     monkeypatch.setattr("builtins.open", fake_open)

#     from pathlib import Path
#     real_read_text = Path.read_text

#     def fake_read_text(self, *args, **kwargs):
#         if str(self).endswith("spamshield-advisor-system-prompt.md"):
#             return FAKE_SYSTEM_PROMPT
#         return real_read_text(self, *args, **kwargs)

#     monkeypatch.setattr(Path, "read_text", fake_read_text)


# # ---------- Jeux de données réels, mais redirigés vers les fixtures de test ----------

# @pytest.fixture(autouse=True)
# def use_test_corpus(monkeypatch):
#     """Redirige toute lecture de corpus.parquet ou spam_ham_dataset.parquet vers les
#     fixtures versionnées dans tests/test_ressources/, plutôt que vers les fichiers de
#     production (non versionnés) ou un mock qui viderait le comportement réel du
#     détecteur de charabia. Le vrai code de Metadata_Business_Rules / Business_Rules
#     s'exécute donc normalement, juste avec des données de test contrôlées."""
#     real_read_parquet = pd.read_parquet

#     def fake_read_parquet(path, *args, **kwargs):
#         path_str = str(path)
#         if path_str.endswith("corpus.parquet"):
#             return real_read_parquet(os.path.join(TEST_RESOURCES_DIR, "corpus.parquet"), *args, **kwargs)
#         if path_str.endswith("spam_ham_dataset.parquet"):
#             return real_read_parquet(os.path.join(TEST_RESOURCES_DIR, "spam_ham_dataset.parquet"), *args, **kwargs)
#         return real_read_parquet(path, *args, **kwargs)

#     monkeypatch.setattr(pd, "read_parquet", fake_read_parquet)