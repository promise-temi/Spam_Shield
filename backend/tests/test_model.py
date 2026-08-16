"""
Tests du modele de classification SpamShield (competence C12).
"""

import os
import sys

import numpy as np
import pandas as pd
import pytest

from unittest.mock import patch


# ============================================================
# PATH
# ============================================================

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
# NEUTRALISER MLFLOW AVANT IMPORT DE MODEL
# ============================================================

with patch("mlflow.set_tracking_uri"), \
     patch("mlflow.set_experiment"):

    from modules.Model import Model


# ============================================================
# RESSOURCES DE TEST
# ============================================================

TEST_CORPUS = "backend/tests/test_ressources/corpus.parquet"
TEST_ARTIFACT_DIR = "backend/tests/test_ressources"


# ============================================================
# FIXTURE
# VRAI ENTRAINEMENT LOCAL
# MAIS AUCUNE COMMUNICATION AVEC MLFLOW
# ============================================================

@pytest.fixture(scope="session")
def modele_entraine():

    with patch("modules.Model.mlflow.start_run"), \
         patch("modules.Model.ML_Flow_Operations"), \
         patch("Preprocessing.ML_Flow_Operations"), \
         patch("mlflow.log_artifact"), \
         patch("mlflow.log_metric"), \
         patch("mlflow.sklearn.log_model"):

        model = Model()

        model.corpus_path = TEST_CORPUS
        model.artifact_path = TEST_ARTIFACT_DIR

        model.AI_full_virgin_model_training_pipeline()

    return TEST_ARTIFACT_DIR


# ============================================================
# MODELE DE PREDICTION
# ============================================================

def _model_de_prediction():

    model = Model(
        prediction_pipe=True,
        seuil_confiance=False
    )

    model.corpus_path = TEST_CORPUS
    model.artifact_path = TEST_ARTIFACT_DIR

    return model


# ============================================================
# DONNEES DE TEST
# ============================================================

SPAMS_EVIDENTS = [
    (
        "GAGNEZ 10000 euros MAINTENANT !!! "
        "Cliquez ici : http://arnaque.xyz "
        "argent gratuit crypto bitcoin"
    ),
    (
        "Felicitations vous avez gagne un iPhone gratuit, "
        "urgent reclamez votre cadeau maintenant !!!"
    ),
]


HAMS_EVIDENTS = [
    (
        "Bonjour, je souhaiterais obtenir un devis pour "
        "la renovation de ma salle de bain. Cordialement."
    ),
    (
        "Bonjour, suite a notre rendez-vous de mardi, "
        "pourriez-vous me confirmer l'horaire ? Merci."
    ),
]


# ============================================================
# TESTS SPAM
# ============================================================

@pytest.mark.parametrize(
    "message",
    SPAMS_EVIDENTS
)
def test_garde_fou_spam_evident_est_classe_spam(
    message,
    modele_entraine
):

    model = _model_de_prediction()

    df = pd.DataFrame(
        [
            {
                "text": message
            }
        ]
    )

    pred = model.AI_full_prediction_pipeline(df)

    assert int(pred[0]) == 1, (
        f"Spam evident classe HAM : {message!r}"
    )


# ============================================================
# TESTS HAM
# ============================================================

@pytest.mark.parametrize(
    "message",
    HAMS_EVIDENTS
)
def test_garde_fou_ham_evident_est_classe_ham(
    message,
    modele_entraine
):

    model = _model_de_prediction()

    df = pd.DataFrame(
        [
            {
                "text": message
            }
        ]
    )

    pred = model.AI_full_prediction_pipeline(df)

    assert int(pred[0]) == 0, (
        f"Ham evident classe SPAM : {message!r}"
    )


# ============================================================
# OVERRIDE
# ============================================================

def test_override_bascule_ham_incertain_en_spam():

    model = Model()

    pred = np.array([0])

    out = model.confidence_based_pred(
        pred,
        confidence=0.45
    )

    assert (
        out[0] == 1
        and model.override is True
    )


def test_override_ne_touche_pas_une_prediction_confiante():

    model = Model()

    pred = np.array([0])

    out = model.confidence_based_pred(
        pred,
        confidence=0.95
    )

    assert (
        out[0] == 0
        and model.override is False
    )