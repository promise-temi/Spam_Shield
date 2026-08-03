import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Markov_Model import MarkovGibberishDetector


CORPUS = "bonjour comment allez vous je suis intéressé par votre produit merci beaucoup pour votre réponse rapide"


@pytest.fixture
def detector_entraine():
    detector = MarkovGibberishDetector()
    detector.train_model(CORPUS.split())
    return detector


def test_score_texte_trop_court_retourne_zero(detector_entraine):
    """Un texte de moins de 2 caractères ne peut pas produire de transitions."""
    assert detector_entraine.markov_score("a") == 0


def test_detecteur_non_entraine_considere_tout_comme_gibberish():
    """Sans entraînement, toutes les probabilités de transition valent 0 :
    le score est donc toujours 0, et 0 < seuil (0.06) => is_gibberish = True."""
    detector = MarkovGibberishDetector()
    assert detector.is_gibberish("bonjour comment allez vous") is True


def test_texte_coherent_proche_du_corpus_nest_pas_gibberish(detector_entraine):
    assert detector_entraine.is_gibberish("bonjour comment allez vous") is False


def test_texte_aleatoire_est_detecte_comme_gibberish(detector_entraine):
    assert detector_entraine.is_gibberish("xzqjw kvbnm ptrfl") is True


def test_clean_text_supprime_ponctuation_chiffres_garde_accents():
    detector = MarkovGibberishDetector()
    result = detector.clean_text("Bonjour!! 123 café, ça va??")
    assert result == "bonjour café ça va"


def test_seuil_est_configurable():
    """Avec un seuil à 0, même un score très faible ne doit jamais être détecté comme gibberish."""
    detector = MarkovGibberishDetector()
    detector.train_model(CORPUS.split())
    assert detector.is_gibberish("xzqjw kvbnm ptrfl", threshold=0) is False