import os
import sys
import numpy as np
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Model import Model


def test_override_quand_confiance_insuffisante():
    model = Model()
    pred = np.array([0])  # le modèle prédit "légitime"
    result = model.confidence_based_pred(pred, confidence=0.45)
    assert result[0] == 1  # reclassé en spam
    assert model.override is True


def test_override_a_la_limite_exacte_60_pourcent():
    """La condition du code est <=0.60 : la limite doit déclencher l'override."""
    model = Model()
    pred = np.array([0])
    result = model.confidence_based_pred(pred, confidence=0.60)
    assert result[0] == 1
    assert model.override is True


def test_pas_override_juste_au_dessus_de_60_pourcent():
    model = Model()
    pred = np.array([0])
    result = model.confidence_based_pred(pred, confidence=0.61)
    assert result[0] == 0
    assert model.override is False


def test_pas_override_si_confiance_elevee():
    model = Model()
    pred = np.array([0])
    result = model.confidence_based_pred(pred, confidence=0.95)
    assert result[0] == 0
    assert model.override is False


def test_pas_override_si_deja_predit_spam():
    """Le mécanisme d'override ne s'applique qu'aux prédictions 'légitime' :
    un message déjà prédit comme spam ne doit jamais être reclassé, même avec
    une confiance nulle."""
    model = Model()
    pred = np.array([1])  # le modèle prédit déjà "spam"
    result = model.confidence_based_pred(pred, confidence=0.0)
    assert result[0] == 1
    assert model.override is False