"""
Tests du modèle de classification SpamShield (compétence C12).

STRATÉGIE DE TEST
-----------------
Trois familles de tests, chacune avec un périmètre et une intention distincts :

1. TUYAUTERIE DES PIPELINES (mockée)
   Objectif : garantir que les pipelines d'entraînement et de réentraînement
   enchaînent correctement leurs étapes (feature engineering -> preprocessing
   -> entraînement -> évaluation -> sauvegarde) et que les garde-fous d'entrée
   se déclenchent. On mocke toutes les I/O (MLflow, disque, sources de données)
   pour tester la logique d'orchestration SANS entraîner de vrai modèle ni
   laisser de trace.

2. GARDE-FOUS QUALITÉ DU MODÈLE (non-régression)
   Objectif : s'assurer qu'on ne met jamais en service un modèle « qui classe
   n'importe quoi ». On soumet des cas volontairement caricaturaux (spam
   évident / ham évident) au modèle réellement sauvegardé et on vérifie qu'il
   les classe correctement. Ces tests ne sont PAS déterministes au sens strict :
   ils dépendent du modèle entraîné. C'est voulu — ce sont des sentinelles de
   non-régression, destinées à échouer si un réentraînement dégrade le modèle
   au point de rater un cas évident.

3. LOGIQUE D'OVERRIDE (déterministe)
   Objectif : vérifier la règle métier de reclassement par seuil de confiance,
   indépendamment du modèle. (Couvert dans test_model_override.py — rappelé ici
   pour la complétude de la stratégie.)

Lancer : pytest test_model.py -v
Le garde-fou qualité nécessite un modèle entraîné ; il est ignoré (skip) proprement
si aucun model.pkl n'est disponible, plutôt que d'échouer pour une mauvaise raison.
"""

import os
import sys
import numpy as np
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Model import Model


# ===========================================================================
# FAMILLE 1 — TUYAUTERIE DES PIPELINES (tout mocké, aucune trace)
# ===========================================================================

@patch("Model.ML_Flow_Operations")
@patch("Model.Preprocessing")
@patch("Model.NLP_Feat_Eng")
@patch("Model.SET_Spam_Shield_Dependances")
@patch("Model.mlflow")
def test_pipeline_entrainement_vierge_enchaine_les_etapes(
    mock_mlflow, mock_deps, mock_feat_eng, mock_preprocessing, mock_mlflow_ops
):
    """Le pipeline d'entraînement vierge doit : charger les données, faire le
    feature engineering, le preprocessing, entraîner/évaluer/sauvegarder, puis
    logger les métriques — sans qu'aucune vraie I/O ne soit exécutée."""

    # Données factices suffisantes (>= 10 lignes pour passer le garde-fou)
    fake_training_data = pd.DataFrame({"text": ["msg"] * 12, "label": [0, 1] * 6})
    mock_deps.return_value.Dependances_Full_Pipeline.return_value = fake_training_data

    # Le feature engineering renvoie un DataFrame quelconque
    mock_feat_eng.return_value.feature_engineering_full_pipeline.return_value = fake_training_data

    # Le preprocessing renvoie des matrices factices (train/test/labels/weights)
    X_train = np.zeros((8, 5))
    X_test = np.zeros((2, 5))
    y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    y_test = np.array([0, 1])
    mock_preprocessing.return_value.preprocessing_pipeline.return_value = (
        X_train, X_test, y_train, y_test, None, None
    )

    # mlflow.start_run doit se comporter comme un context manager
    mock_mlflow.start_run.return_value.__enter__.return_value = MagicMock()

    model = Model()
    # On mocke l'entraînement réel du classifieur pour ne rien calculer
    with patch.object(model, "build_virgin_model_pipeline", return_value={"accuracy": 0.9}) as mock_build:
        model.AI_full_virgin_model_training_pipeline()

    # Les étapes clés ont bien été appelées, dans le bon esprit
    mock_deps.return_value.Dependances_Full_Pipeline.assert_called_once()
    mock_feat_eng.return_value.feature_engineering_full_pipeline.assert_called_once()
    mock_preprocessing.return_value.preprocessing_pipeline.assert_called_once()
    mock_build.assert_called_once()
    mock_mlflow_ops.return_value.save_metrics.assert_called_once_with({"accuracy": 0.9})


@patch("Model.SET_Spam_Shield_Dependances")
def test_pipeline_entrainement_refuse_moins_de_10_lignes(mock_deps):
    """Garde-fou : moins de 10 lignes de données doit lever une ValueError
    explicite plutôt que d'entraîner un modèle sur un échantillon ridicule."""
    fake_small = pd.DataFrame({"text": ["a", "b"], "label": [0, 1]})
    mock_deps.return_value.Dependances_Full_Pipeline.return_value = fake_small

    model = Model()
    with pytest.raises(ValueError, match="au moins 10 lignes"):
        model.AI_full_virgin_model_training_pipeline()


@patch("Model.ML_Flow_Operations")
@patch("Model.Preprocessing")
@patch("Model.NLP_Feat_Eng")
@patch("Model.mlflow")
def test_pipeline_reentrainement_enchaine_les_etapes(
    mock_mlflow, mock_feat_eng, mock_preprocessing, mock_mlflow_ops
):
    """Le pipeline de réentraînement doit recharger le dernier modèle, le
    réentraîner sur les nouvelles données (avec sample_weight), évaluer et logger."""

    fake_new_data = pd.DataFrame({"text": ["msg"] * 12, "label": [0, 1] * 6})
    mock_feat_eng.return_value.feature_engineering_full_pipeline.return_value = fake_new_data

    X_train = np.zeros((8, 5))
    X_test = np.zeros((2, 5))
    y_train = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    y_test = np.array([0, 1])
    s_weight = np.array([3.0] * 8)
    mock_preprocessing.return_value.preprocessing_pipeline.return_value = (
        X_train, X_test, y_train, y_test, s_weight, None
    )

    mock_mlflow.start_run.return_value.__enter__.return_value = MagicMock()

    # Le "dernier modèle" rechargé depuis MLflow est un mock entraînable
    mock_loaded_model = MagicMock()
    mock_loaded_model.predict.return_value = y_test
    mock_mlflow_ops.return_value.get_latest_model.return_value = mock_loaded_model

    model = Model()
    with patch.object(model, "evaluate_model", return_value={"accuracy": 0.88}) as mock_eval, \
         patch.object(model, "save_model_mlflow"), \
         patch.object(model, "save_model_local"):
        model.AI_full_retrain_model_pipeline(fake_new_data)

    # Le modèle rechargé a bien été réentraîné avec les poids, puis évalué
    mock_loaded_model.fit.assert_called_once()
    _, kwargs = mock_loaded_model.fit.call_args
    assert "sample_weight" in kwargs  # le poids renforcé des nouvelles données est transmis
    mock_eval.assert_called_once()
    mock_mlflow_ops.return_value.save_metrics.assert_called_once_with({"accuracy": 0.88})


def test_pipeline_reentrainement_refuse_moins_de_10_lignes():
    """Même garde-fou côté réentraînement."""
    model = Model()
    df_small = pd.DataFrame({"text": ["a", "b"], "label": [0, 1]})
    with pytest.raises(ValueError, match="au moins 10 lignes"):
        model.AI_full_retrain_model_pipeline(df_small)


# ===========================================================================
# FAMILLE 2 — GARDE-FOUS QUALITÉ (non-régression sur cas caricaturaux)
# ===========================================================================
# Ces tests soumettent des messages évidents au VRAI pipeline de prédiction.
# Ils valident qu'on ne met pas en service un modèle « qui pue ».
# Ils sont ignorés proprement si aucun modèle n'est encore entraîné.

MODEL_PKL = os.path.join(
    os.path.dirname(__file__), "..", "modules", "data", "model.pkl"
)

modele_absent = not os.path.exists(MODEL_PKL)
skip_si_pas_de_modele = pytest.mark.skipif(
    modele_absent,
    reason="Aucun model.pkl entraîné disponible — garde-fou qualité ignoré."
)

# Cas volontairement caricaturaux : la vérité terrain ne fait aucun doute.
SPAMS_EVIDENTS = [
    "GAGNEZ 10000€ MAINTENANT !!! Cliquez ici : http://arnaque.xyz argent gratuit crypto bitcoin",
    "Félicitations vous avez gagné un iPhone gratuit, urgent réclamez votre cadeau maintenant !!!",
]
HAMS_EVIDENTS = [
    "Bonjour, je souhaiterais obtenir un devis pour la rénovation de ma salle de bain. Cordialement.",
    "Bonjour, suite à notre rendez-vous de mardi, pourriez-vous me confirmer l'horaire ? Merci.",
]


@skip_si_pas_de_modele
@pytest.mark.parametrize("message", SPAMS_EVIDENTS)
def test_garde_fou_spam_evident_est_classe_spam(message):
    """Un spam caricatural doit être classé spam (label 1).
    NON déterministe par nature : sentinelle de non-régression. S'il échoue,
    c'est un signal que le modèle mis en service s'est dégradé."""
    model = Model(prediction_pipe=True, seuil_confiance=False)
    df = pd.DataFrame([{"text": message}])
    pred = model.AI_full_prediction_pipeline(df)
    assert int(pred[0]) == 1, f"Spam évident classé HAM : {message!r}"


@skip_si_pas_de_modele
@pytest.mark.parametrize("message", HAMS_EVIDENTS)
def test_garde_fou_ham_evident_est_classe_ham(message):
    """Un message légitime caricatural doit être classé ham (label 0),
    override désactivé pour isoler la décision brute du modèle."""
    model = Model(prediction_pipe=True, seuil_confiance=False)
    df = pd.DataFrame([{"text": message}])
    pred = model.AI_full_prediction_pipeline(df)
    assert int(pred[0]) == 0, f"Ham évident classé SPAM : {message!r}"


# ===========================================================================
# FAMILLE 3 — LOGIQUE D'OVERRIDE (déterministe, rappel)
# ===========================================================================
# Le détail complet est dans test_model_override.py. On vérifie ici a minima
# que la règle de seuil se comporte comme attendu, pour que ce fichier couvre
# à lui seul la stratégie annoncée en en-tête.

def test_override_bascule_ham_incertain_en_spam():
    model = Model()
    pred = np.array([0])              # prédit "légitime"
    out = model.confidence_based_pred(pred, confidence=0.45)  # sous le seuil
    assert out[0] == 1 and model.override is True


def test_override_ne_touche_pas_une_prediction_confiante():
    model = Model()
    pred = np.array([0])
    out = model.confidence_based_pred(pred, confidence=0.95)
    assert out[0] == 0 and model.override is False
