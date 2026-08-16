import os
import sys
import pytest

from unittest.mock import patch


# Permet d'importer backend/modules depuis les tests
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


# ============================================================
# MODELE DE TEST
# ============================================================

@pytest.fixture
def test_model():
    from modules.Model import Model

    model = Model()

    model.corpus_path = (
        "backend/tests/test_ressources/corpus.parquet"
    )

    model.artifact_path = (
        "backend/tests/test_ressources"
    )

    return model


@pytest.fixture
def test_model_pred():
    from modules.Model import Model

    metadata = {
        "name": "Jane",
        "surname": "Doe",
        "email": "Jane.Doe@email.com",
        "phone": "0605678978",
        "subject": "Ceci est un test",
        "form_id": "test"
    }

    model = Model(
        prediction_pipe=True,
        metadata=metadata
    )

    model.corpus_path = (
        "backend/tests/test_ressources/corpus.parquet"
    )

    model.artifact_path = (
        "backend/tests/test_ressources"
    )

    return model


# ============================================================
# METADATA BUSINESS RULES
# ============================================================

@pytest.fixture
def test_metadata_path():
    from modules.Metadata_Business_Rules import (
        Metadata_Business_Rules
    )

    return Metadata_Business_Rules(
        "backend/tests/test_ressources/required_metadata.json"
    )


# ============================================================
# DATABASE TEST
# ============================================================

@pytest.fixture
def test_db():
    from modules.Database import Postgres_DB

    db = Postgres_DB(
        sql_file_path="backend/modules/data/db.sql",
        prod=False
    )

    return db


# ============================================================
# PROMETHEUS
# ============================================================

@pytest.fixture
def mock_monitor():
    with patch(
        "modules.SpamShield_Operations.monitor"
    ) as mock:
        yield mock


# ============================================================
# MLFLOW - PREPROCESSING
# ============================================================

@pytest.fixture
def mock_preprocessing_mlflow():
    with patch(
        "modules.Preprocessing.ML_Flow_Operations"
    ) as mock:
        yield mock


# ============================================================
# MLFLOW - MODEL
# ============================================================

@pytest.fixture
def mock_model_mlflow():
    with patch(
        "modules.Model.ML_Flow_Operations"
    ) as mock:
        yield mock


# ============================================================
# MLFLOW START RUN
# ============================================================

@pytest.fixture
def mock_mlflow_run():
    with patch(
        "modules.Model.mlflow.start_run"
    ):
        yield


# ============================================================
# SPAMSHIELD OPERATIONS
# ============================================================
@pytest.fixture
def spamshield(test_db, monkeypatch):

    # Neutralise la configuration MLflow AVANT
    # l'import de SpamShield_Operations
    with patch("mlflow.set_tracking_uri"), \
         patch("mlflow.set_experiment"):

        from modules.SpamShield_Operations import SpamShield_Operations

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    return SpamShield_Operations()