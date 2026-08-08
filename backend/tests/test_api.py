from unittest.mock import patch

HEADERS_KO = {"x-api-key": "mauvaise-cle"}



# ---------- Comportement fonctionnel (client AVEC override, l'auth n'est plus le sujet) ----------

@patch("api.SpamShield_Operations")
def test_dashboard_metrics_retourne_la_structure_attendue(mock_ops, client):
    mock_ops.return_value.Dashbord.return_value = {"messages": 6, "spam": 3, "ham": 3}
    response = client.get("/dashboard-metrics")
    data = response.json()
    assert "metrics" in data
    assert data["metrics"]["messages"] == 6


@patch("api.SpamShield_Operations")
def test_new_message_appelle_bien_le_pipeline(mock_ops, client):
    payload = {
        "message": "Bonjour, je suis intéressé par vos services.",
        "metadata": {"name": "Jean", "surname": "Dupont", "email": "jean@test.com",
                      "phone": "0600000000", "subject": "Contact", "form_id": "1"},
        "settings": {"entrainementModel": False, "recevoirParMail": False},
    }
    response = client.post("/new-message", json=payload)
    assert response.status_code == 200
    mock_ops.return_value.New_Message.assert_called_once()


@patch("api.SpamShield_Operations")
def test_new_message_rejette_un_payload_invalide(mock_ops, client):
    response = client.post("/new-message", json={"metadata": {}})
    assert response.status_code == 422
    mock_ops.return_value.New_Message.assert_not_called()


@patch("api.SpamShield_Operations")
def test_build_virgin_model_declenche_bien_le_reset(mock_ops, client):
    response = client.get("/build_virgin_model")
    assert response.status_code == 200
    mock_ops.return_value.virgin_model.assert_called_once()


@patch("api.LLMModel")
def test_llm_report_appelle_mistral_et_pas_le_vrai_service(mock_llm, client):
    mock_llm.return_value.generate_report_mistral.return_value = {
        "model_used": "mistral-small-2603",
        "llm_response": "Rapport simulé.",
        "base_metrics": {},
    }
    response = client.get("/llm-report")
    assert response.status_code == 200
    assert response.json()["llm_response"] == "Rapport simulé."













"""
Tests pytest pour l'API SpamShield.

Chaque route est testée selon trois axes quand c'est pertinent :
  - accès refusé sans clé API valide (401)
  - cas de succès (200), avec la couche métier mockée
  - cas d'erreur interne (500), pour vérifier que le try/except
    de chaque route capture bien l'exception et répond proprement

Lancer avec : pytest -v
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)

VALID_HEADERS = {"x-api-key": "une-cle-valide"}
INVALID_HEADERS = {"x-api-key": "une-cle-invalide"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def mock_security():
    """
    Simule la vérification de la clé API pour tous les tests :
    la clé 'une-cle-valide' est acceptée, toute autre est refusée.
    """
    with patch("api.security.verify_api_key") as mock_verify:
        mock_verify.side_effect = lambda key: key == "une-cle-valide"
        yield mock_verify


# ---------------------------------------------------------------------------
# Authentification (commune à toutes les routes protégées)
# ---------------------------------------------------------------------------

def test_route_sans_cle_api_retourne_401():
    response = client.get("/dashboard-metrics")
    assert response.status_code == 422  # header requis manquant


def test_route_avec_cle_api_invalide_retourne_401():
    response = client.get("/dashboard-metrics", headers=INVALID_HEADERS)
    assert response.status_code == 401
    assert "Clé API invalide" in response.json()["detail"]


# ---------------------------------------------------------------------------
# /dashboard-metrics
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_dashboard_metrics_succes(mock_ops):
    mock_ops.return_value.Dashbord.return_value = {"messages": 6, "spam": 3}

    response = client.get("/dashboard-metrics", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json() == {"metrics": {"messages": 6, "spam": 3}}


@patch("api.SpamShield_Operations")
def test_dashboard_metrics_erreur_interne(mock_ops):
    mock_ops.return_value.Dashbord.side_effect = Exception("Connexion PostgreSQL perdue")

    response = client.get("/dashboard-metrics", headers=VALID_HEADERS)

    assert response.status_code == 500
    assert "Connexion PostgreSQL perdue" in response.json()["detail"]


# ---------------------------------------------------------------------------
# /get-messages/{trier_par}/{filtrer_par}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_all_messages_succes(mock_ops):
    mock_ops.return_value.Show_Messages.return_value = [{"id": 1, "label": "ham"}]

    response = client.get("/get-messages/date/tous", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["messages"] == [{"id": 1, "label": "ham"}]
    mock_ops.return_value.Show_Messages.assert_called_once_with("date", "tous")


@patch("api.SpamShield_Operations")
def test_get_all_messages_erreur_interne(mock_ops):
    mock_ops.return_value.Show_Messages.side_effect = Exception("Filtre invalide")

    response = client.get("/get-messages/date/tous", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /get_message-and-related-metrics/{selected_message_id}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_message_and_related_metrics_succes(mock_ops):
    mock_ops.return_value.Select_Message.return_value = {"id": 42, "label_final": "spam"}

    response = client.get("/get_message-and-related-metrics/42", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["selected_message"]["id"] == 42


@patch("api.SpamShield_Operations")
def test_get_message_and_related_metrics_id_inexistant(mock_ops):
    mock_ops.return_value.Select_Message.side_effect = Exception("Message introuvable")

    response = client.get("/get_message-and-related-metrics/9999", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /update_label/{id}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_update_label_succes(mock_ops):
    response = client.get("/update_label/1", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
    mock_ops.return_value.Update_label.assert_called_once_with(1)


@patch("api.SpamShield_Operations")
def test_update_label_erreur_interne(mock_ops):
    mock_ops.return_value.Update_label.side_effect = Exception("Écriture impossible")

    response = client.get("/update_label/1", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /new-message
# ---------------------------------------------------------------------------

VALID_MESSAGE_PAYLOAD = {
    "message": "Bonjour, je souhaite un devis.",
    "metadata": {
        "name": "Dupont",
        "surname": "Jean",
        "email": "jean.dupont@example.com",
        "phone": "0600000000",
        "subject": "Demande de devis",
        "form_id": "contact-1",
    },
    "settings": {
        "entrainementModel": True,
        "recevoirParMail": False,
    },
}


@patch("api.SpamShield_Operations")
def test_new_message_succes(mock_ops):
    response = client.post("/new-message", json=VALID_MESSAGE_PAYLOAD, headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
    mock_ops.return_value.New_Message.assert_called_once()


def test_new_message_payload_invalide():
    payload_invalide = {"message": "texte sans metadata ni settings"}

    response = client.post("/new-message", json=payload_invalide, headers=VALID_HEADERS)

    assert response.status_code == 422  # erreur de validation Pydantic


@patch("api.SpamShield_Operations")
def test_new_message_erreur_interne(mock_ops):
    mock_ops.return_value.New_Message.side_effect = Exception("Échec de la classification")

    response = client.post("/new-message", json=VALID_MESSAGE_PAYLOAD, headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /get-regexes, /new-regex, /delete-regex/{id}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_regexes_succes(mock_ops):
    mock_ops.return_value.Get_All_Regex_Rules.return_value = ["viagra", "casino"]

    response = client.get("/get-regexes", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["regex_rules"] == ["viagra", "casino"]


@patch("api.SpamShield_Operations")
def test_new_regex_succes(mock_ops):
    response = client.post("/new-regex", json={"pattern": "crypto.*gratuit"}, headers=VALID_HEADERS)

    assert response.status_code == 200
    mock_ops.return_value.Add_Regex_Rule.assert_called_once_with("crypto.*gratuit")


@patch("api.SpamShield_Operations")
def test_new_regex_erreur_interne(mock_ops):
    mock_ops.return_value.Add_Regex_Rule.side_effect = Exception("Regex mal formée")

    response = client.post("/new-regex", json={"pattern": "("}, headers=VALID_HEADERS)

    assert response.status_code == 500


@patch("api.SpamShield_Operations")
def test_delete_regex_succes(mock_ops):
    response = client.delete("/delete-regex/3", headers=VALID_HEADERS)

    assert response.status_code == 200
    mock_ops.return_value.Delete_Regex_Rule.assert_called_once_with(3)


@patch("api.SpamShield_Operations")
def test_delete_regex_erreur_interne(mock_ops):
    mock_ops.return_value.Delete_Regex_Rule.side_effect = Exception("Règle introuvable")

    response = client.delete("/delete-regex/999", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /get-detinataires, /new-detinataires, /delete-destinataire/{id}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_detinataires_succes(mock_ops):
    mock_ops.return_value.Get_All_Destinataires.return_value = ["contact@spamshield.fr"]

    response = client.get("/get-detinataires", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["destinataires"] == ["contact@spamshield.fr"]


@patch("api.SpamShield_Operations")
def test_new_detinataires_succes(mock_ops):
    response = client.post(
        "/new-detinataires", json={"destinataire": "alerte@spamshield.fr"}, headers=VALID_HEADERS
    )

    assert response.status_code == 200
    mock_ops.return_value.Add_Destinataire.assert_called_once_with("alerte@spamshield.fr")


@patch("api.SpamShield_Operations")
def test_new_detinataires_erreur_interne(mock_ops):
    mock_ops.return_value.Add_Destinataire.side_effect = Exception("Adresse déjà existante")

    response = client.post(
        "/new-detinataires", json={"destinataire": "alerte@spamshield.fr"}, headers=VALID_HEADERS
    )

    assert response.status_code == 500


@patch("api.SpamShield_Operations")
def test_delete_destinataire_succes(mock_ops):
    response = client.delete("/delete-destinataire/2", headers=VALID_HEADERS)

    assert response.status_code == 200
    mock_ops.return_value.Delete_Destinataire.assert_called_once_with(2)


@patch("api.SpamShield_Operations")
def test_delete_destinataire_erreur_interne(mock_ops):
    mock_ops.return_value.Delete_Destinataire.side_effect = Exception("Destinataire introuvable")

    response = client.delete("/delete-destinataire/999", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /get-champs-obligatoires-status, /update-champs-obligatoires-status/{key}
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_champs_obligatoire_status_succes(mock_ops):
    mock_ops.return_value.Form_Requirements.return_value = {"nom": True, "email": True}

    response = client.get("/get-champs-obligatoires-status", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["form_requirements"]["email"] is True


@patch("api.SpamShield_Operations")
def test_update_champs_obligatoire_status_succes(mock_ops):
    response = client.put("/update-champs-obligatoires-status/email", headers=VALID_HEADERS)

    assert response.status_code == 200
    mock_ops.return_value.Update_Form_Requirements.assert_called_once_with("email")


@patch("api.SpamShield_Operations")
def test_update_champs_obligatoire_status_erreur_interne(mock_ops):
    mock_ops.return_value.Update_Form_Requirements.side_effect = Exception("Clé de champ inconnue")

    response = client.put("/update-champs-obligatoires-status/inconnu", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /get-ai-model-infos
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_get_ai_model_infos_succes(mock_ops):
    mock_ops.return_value.Current_Model_Metrics.return_value = {"accuracy": 0.94}

    response = client.get("/get-ai-model-infos", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["spamshield_infos"]["accuracy"] == 0.94


@patch("api.SpamShield_Operations")
def test_get_ai_model_infos_erreur_interne(mock_ops):
    mock_ops.return_value.Current_Model_Metrics.side_effect = Exception("Aucun modèle entraîné")

    response = client.get("/get-ai-model-infos", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /build_virgin_model
# ---------------------------------------------------------------------------

@patch("api.SpamShield_Operations")
def test_reset_ai_model_succes(mock_ops):
    response = client.get("/build_virgin_model", headers=VALID_HEADERS)

    assert response.status_code == 200
    mock_ops.return_value.virgin_model.assert_called_once()


@patch("api.SpamShield_Operations")
def test_reset_ai_model_erreur_interne(mock_ops):
    mock_ops.return_value.virgin_model.side_effect = Exception("Réinitialisation impossible")

    response = client.get("/build_virgin_model", headers=VALID_HEADERS)

    assert response.status_code == 500


# ---------------------------------------------------------------------------
# /llm-report — la route testée en partie 4.7 du rapport (Swagger)
# ---------------------------------------------------------------------------

@patch("api.LLMModel")
def test_llm_report_succes(mock_llm_model):
    mock_llm_model.return_value.generate_report_mistral.return_value = {
        "model_used": "mistral-small-2603",
        "llm_response": "État général : le système a reçu 6 messages...",
        "base_metrics": {"messages": 6},
    }

    response = client.get("/llm-report", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["model_used"] == "mistral-small-2603"


@patch("api.LLMModel")
def test_llm_report_cle_api_mistral_expiree(mock_llm_model):
    """
    Reproduit l'incident réel rencontré en monitorage (partie 4.6/4.8) :
    la clé API Mistral a expiré, l'appel échoue avec une erreur 401
    remontée par le SDK, capturée par le try/except de la route.
    """
    mock_llm_model.return_value.generate_report_mistral.side_effect = Exception(
        'API error occurred: Status 401. Body: {"detail":"Your API key expired on 2026-08-03."}'
    )

    response = client.get("/llm-report", headers=VALID_HEADERS)

    assert response.status_code == 500
    assert "expired" in response.json()["detail"]