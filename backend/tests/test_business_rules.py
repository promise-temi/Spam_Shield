import os
import sys
import pytest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
import Business_Rules as business_rules_module
from Business_Rules import Business_Rules


@pytest.fixture
def make_business_rules(monkeypatch):
    """Fabrique de Business_Rules avec la connexion PostgreSQL toujours simulée,
    quels que soient les paramètres passés à chaque test."""
    fake_db = MagicMock()
    fake_db.get_regexes_patterns.return_value = []
    monkeypatch.setattr(business_rules_module, "Postgres_DB", lambda: fake_db)

    def _make(**kwargs):
        return Business_Rules(**kwargs)

    return _make


@pytest.fixture
def business_rules(make_business_rules):
    return make_business_rules(min_lenght_message=5, max_lenght_message=1000)


def test_message_trop_court_est_detecte(business_rules):
    business_rules.filter_message_lenght("abc")
    assert any("trop court" in p for p in business_rules.banned_patterns_found)


def test_message_trop_long_est_detecte(make_business_rules):
    br = make_business_rules(min_lenght_message=5, max_lenght_message=10)
    br.filter_message_lenght("un message clairement beaucoup trop long pour la limite fixée")
    assert any("trop long" in p for p in br.banned_patterns_found)


def test_message_taille_normale_ne_declenche_rien(business_rules):
    business_rules.filter_message_lenght("Ceci est un message de taille tout à fait normale.")
    assert business_rules.banned_patterns_found == []


def test_deliberation_ham_si_aucun_motif(business_rules):
    assert business_rules.delibaration() == 0


def test_deliberation_spam_si_au_moins_un_motif(business_rules):
    business_rules.banned_patterns_found.append("un motif quelconque")
    assert business_rules.delibaration() == 1


def test_banned_patterns_detecte_un_motif_interdit(business_rules):
    business_rules.patterns = [r"http://"]
    business_rules.banned_patterns("http://site-suspect.com")
    assert len(business_rules.banned_patterns_found) == 1


def test_banned_patterns_sans_regle_configuree_ne_detecte_rien(business_rules):
    business_rules.patterns = []
    business_rules.banned_patterns("n'importe quel texte")
    assert business_rules.banned_patterns_found == []


def test_pipeline_complet_message_legitime(business_rules):
    metadata = {"name": None, "surname": None, "email": None, "phone": None, "subject": None}
    result = business_rules.business_rules_pipeline(
        "Ceci est un message parfaitement légitime et normal.", metadata
    )
    assert result == 0