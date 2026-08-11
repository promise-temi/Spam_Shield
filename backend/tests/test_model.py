"""
Tests du modele de classification SpamShield (competence C12).

STRATEGIE DE TEST
-----------------
Trois familles de tests, chacune avec un perimetre et une intention distincts :

1. TUYAUTERIE DES PIPELINES (mockee)
   Garantit que les pipelines d'entrainement et de reentrainement enchainent
   correctement leurs etapes et que les garde-fous d'entree se declenchent.
   Toutes les I/O sont mockees : aucune vraie trace, aucun vrai modele entraine.

2. GARDE-FOUS QUALITE DU MODELE (non-regression sur cas caricaturaux)
   Un VRAI modele est entraine UNE SEULE FOIS pour la session (fixture
   `modele_entraine`, scope="session"), puis on lui soumet des cas volontairement
   caricaturaux (spam evident / ham evident). Ces tests ne sont pas deterministes
   au sens strict : ce sont des sentinelles de non-regression, destinees a echouer
   si un reentrainement degrade le modele au point de rater un cas evident.

3. LOGIQUE D'OVERRIDE (deterministe)
   Verifie la regle metier de reclassement par seuil de confiance,
   independamment du modele.

Lancer : pytest backend/tests/test_model.py -v
"""

import os
import sys
import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.Model import Model


# Chemins des ressources de test (memes que dans les fixtures du conftest)
TEST_CORPUS = "backend/tests/test_ressources/corpus.parquet"
TEST_ARTIFACT_DIR = "backend/tests/test_ressources"


# ===========================================================================
# FIXTURE — entraine UN vrai modele une seule fois pour toute la session
# ===========================================================================

@pytest.fixture(scope="session")
def modele_entraine():
    """Entraine un modele reel UNE SEULE FOIS pour toute la session de test,
    en suivant exactement le pattern des fixtures test_model du conftest :
    on cree le Model puis on redirige corpus_path / artifact_path vers les
    ressources de test AVANT de lancer l'entrainement. MLflow est neutralise.

    Retourne le Model deja entraine et configure, pret pour la prediction."""
    with patch("ML_Flow._ensure_mlflow_configured", lambda: None), \
         patch("ML_Flow.mlflow.log_artifact", lambda *a, **k: None), \
         patch("ML_Flow.mlflow.log_metric", lambda *a, **k: None), \
         patch("ML_Flow.mlflow.sklearn.log_model", lambda *a, **k: None):

        model = Model()
        model.corpus_path = TEST_CORPUS
        model.artifact_path = TEST_ARTIFACT_DIR
        model.AI_full_virgin_model_training_pipeline()

    return TEST_ARTIFACT_DIR


def _model_de_prediction():
    """Cree un Model de prediction configure sur les ressources de test,
    suivant le meme pattern que la fixture test_model_pred du conftest."""
    model = Model(prediction_pipe=True, seuil_confiance=False)
    model.corpus_path = TEST_CORPUS
    model.artifact_path = TEST_ARTIFACT_DIR
    return model





SPAMS_EVIDENTS = [
    "GAGNEZ 10000 euros MAINTENANT !!! Cliquez ici : http://arnaque.xyz argent gratuit crypto bitcoin",
    "Felicitations vous avez gagne un iPhone gratuit, urgent reclamez votre cadeau maintenant !!!",
]
HAMS_EVIDENTS = [
    "Bonjour, je souhaiterais obtenir un devis pour la renovation de ma salle de bain. Cordialement.",
    "Bonjour, suite a notre rendez-vous de mardi, pourriez-vous me confirmer l'horaire ? Merci.",
]


@pytest.mark.parametrize("message", SPAMS_EVIDENTS)
def test_garde_fou_spam_evident_est_classe_spam(message, modele_entraine):
    """Un spam caricatural doit etre classe spam (label 1).
    Sentinelle de non-regression : un echec signale un modele degrade."""
    model = _model_de_prediction()
    df = pd.DataFrame([{"text": message}])
    pred = model.AI_full_prediction_pipeline(df)
    assert int(pred[0]) == 1, f"Spam evident classe HAM : {message!r}"


@pytest.mark.parametrize("message", HAMS_EVIDENTS)
def test_garde_fou_ham_evident_est_classe_ham(message, modele_entraine):
    """Un message legitime caricatural doit etre classe ham (label 0),
    override desactive pour isoler la decision brute du modele."""
    model = _model_de_prediction()
    df = pd.DataFrame([{"text": message}])
    pred = model.AI_full_prediction_pipeline(df)
    assert int(pred[0]) == 0, f"Ham evident classe SPAM : {message!r}"


def test_override_bascule_ham_incertain_en_spam():
    """Une prediction 'legitime' avec une confiance sous le seuil est reclassee spam."""
    model = Model()
    pred = np.array([0])
    out = model.confidence_based_pred(pred, confidence=0.45)
    assert out[0] == 1 and model.override is True


def test_override_ne_touche_pas_une_prediction_confiante():
    """Une prediction 'legitime' avec une confiance elevee n'est pas touchee."""
    model = Model()
    pred = np.array([0])
    out = model.confidence_based_pred(pred, confidence=0.95)
    assert out[0] == 0 and model.override is False