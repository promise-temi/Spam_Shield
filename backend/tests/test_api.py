import os
import sys
import pytest

from unittest.mock import patch


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


# Variables factices de test
os.environ.setdefault(
    "BACKEND_API_KEY",
    "cle-de-test-1234"
)

os.environ.setdefault(
    "ENCRYPTION_KEY",
    "RxdMLSRTwGMYW6gNoAEvlWbdOHI6iDzjssyXCMMzq2I="
)

os.environ.setdefault(
    "MISTRAL_API_KEY",
    "cle-mistral-factice-pour-les-tests"
)


from fastapi.testclient import TestClient


# Neutralise MLflow AVANT import de l'application
with patch("mlflow.set_tracking_uri"), \
     patch("mlflow.set_experiment"):

    with patch(
        "modules.SpamShield_Operations."
        "SpamShield_Operations.check_model_existence"
    ):
        from api import app, require_api_key
# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture
def client():
    """Client avec authentification bypassée — pour tester la logique des routes."""
    app.dependency_overrides[require_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def client_auth_active():
    """Client avec authentification active — pour tester la protection des routes."""
    return TestClient(app)


# ===========================================================================
# 1. PROTECTION — les 16 routes exigent une clé API
# ===========================================================================

ROUTES_PROTEGEES = [
    ("GET",    "/dashboard-metrics"),
    ("GET",    "/get-messages/date/tous"),
    ("GET",    "/get_message-and-related-metrics/1"),
    ("GET",    "/update_label/1"),
    ("POST",   "/new-message"),
    ("GET",    "/get-regexes"),
    ("POST",   "/new-regex"),
    ("DELETE", "/delete-regex/1"),
    ("GET",    "/get-detinataires"),
    ("POST",   "/new-detinataires"),
    ("DELETE", "/delete-destinataire/1"),
    ("GET",    "/get-champs-obligatoires-status"),
    ("PUT",    "/update-champs-obligatoires-status/email"),
    ("GET",    "/get-ai-model-infos"),
    ("GET",    "/build_virgin_model"),
    ("GET",    "/llm-report"),
]


@pytest.mark.parametrize("method,url", ROUTES_PROTEGEES)
def test_route_sans_cle_est_refusee(client_auth_active, method, url):
    """Sans en-tete x-api-key, la route refuse l'acces (422 : header obligatoire manquant)."""
    response = client_auth_active.request(method, url, json={})
    assert response.status_code == 422


@pytest.mark.parametrize("method,url", ROUTES_PROTEGEES)
def test_route_avec_cle_invalide_renvoie_401(client_auth_active, method, url):
    """Avec une cle invalide, la route renvoie 401."""
    with patch("api.security.verify_api_key", return_value=False):
        response = client_auth_active.request(
            method, url, json={}, headers={"x-api-key": "cle-invalide"}
        )
    assert response.status_code == 401


# ===========================================================================
# 2. FONCTIONNEL — chaque route repond correctement (metier mocke)
# ===========================================================================

# -- Tableau de bord --

@patch("api.SpamShield_Operations")
def test_dashboard_metrics(mock_ops, client):
    mock_ops.return_value.Dashbord.return_value = {"messages": 10, "spam": 5}
    r = client.get("/dashboard-metrics")
    assert r.status_code == 200
    assert r.json()["metrics"] == {"messages": 10, "spam": 5}


@patch("api.SpamShield_Operations")
def test_dashboard_metrics_erreur(mock_ops, client):
    mock_ops.return_value.Dashbord.side_effect = Exception("DB indisponible")
    r = client.get("/dashboard-metrics")
    assert r.status_code == 500


# -- Messages --

@patch("api.SpamShield_Operations")
def test_get_all_messages(mock_ops, client):
    mock_ops.return_value.Show_Messages.return_value = [{"id": 1, "label": "ham"}]
    r = client.get("/get-messages/date/tous")
    assert r.status_code == 200
    assert r.json()["messages"] == [{"id": 1, "label": "ham"}]
    mock_ops.return_value.Show_Messages.assert_called_once_with("date", "tous")


@patch("api.SpamShield_Operations")
def test_get_message_and_related_metrics(mock_ops, client):
    mock_ops.return_value.Select_Message.return_value = {"id": 42}
    r = client.get("/get_message-and-related-metrics/42")
    assert r.status_code == 200
    assert r.json()["selected_message"]["id"] == 42
    mock_ops.return_value.Select_Message.assert_called_once_with(42)


@patch("api.SpamShield_Operations")
def test_update_label(mock_ops, client):
    r = client.get("/update_label/7")
    assert r.status_code == 200
    assert r.json() == {"message": "ok"}
    mock_ops.return_value.Update_label.assert_called_once_with(7)


# -- New message (route critique) --

PAYLOAD_VALIDE = {
    "message": "Bonjour, je souhaite un devis.",
    "metadata": {
        "name": "Dupont", "surname": "Jean",
        "email": "jean.dupont@example.com", "phone": "0600000000",
        "subject": "Devis", "form_id": "contact-1",
    },
    "settings": {"entrainementModel": True, "recevoirParMail": False},
}


@patch("api.SpamShield_Operations")
def test_new_message(mock_ops, client):
    r = client.post("/new-message", json=PAYLOAD_VALIDE)
    assert r.status_code == 200
    assert r.json() == {"message": "ok"}
    mock_ops.return_value.New_Message.assert_called_once()


def test_new_message_payload_invalide(client):
    r = client.post("/new-message", json={"message": "texte seul"})
    assert r.status_code == 422


@patch("api.SpamShield_Operations")
def test_new_message_erreur(mock_ops, client):
    mock_ops.return_value.New_Message.side_effect = Exception("Echec classification")
    r = client.post("/new-message", json=PAYLOAD_VALIDE)
    assert r.status_code == 500


# -- Regex --

@patch("api.SpamShield_Operations")
def test_get_regexes(mock_ops, client):
    mock_ops.return_value.Get_All_Regex_Rules.return_value = ["casino", "viagra"]
    r = client.get("/get-regexes")
    assert r.status_code == 200
    assert r.json()["regex_rules"] == ["casino", "viagra"]


@patch("api.SpamShield_Operations")
def test_new_regex(mock_ops, client):
    r = client.post("/new-regex", json={"pattern": "crypto.*gratuit"})
    assert r.status_code == 200
    mock_ops.return_value.Add_Regex_Rule.assert_called_once_with("crypto.*gratuit")


def test_new_regex_payload_invalide(client):
    r = client.post("/new-regex", json={})
    assert r.status_code == 422


@patch("api.SpamShield_Operations")
def test_delete_regex(mock_ops, client):
    r = client.delete("/delete-regex/3")
    assert r.status_code == 200
    mock_ops.return_value.Delete_Regex_Rule.assert_called_once_with(3)


# -- Destinataires --

@patch("api.SpamShield_Operations")
def test_get_detinataires(mock_ops, client):
    mock_ops.return_value.Get_All_Destinataires.return_value = ["contact@spamshield.fr"]
    r = client.get("/get-detinataires")
    assert r.status_code == 200
    assert r.json()["destinataires"] == ["contact@spamshield.fr"]


@patch("api.SpamShield_Operations")
def test_new_detinataires(mock_ops, client):
    r = client.post("/new-detinataires", json={"destinataire": "alerte@spamshield.fr"})
    assert r.status_code == 200
    mock_ops.return_value.Add_Destinataire.assert_called_once_with("alerte@spamshield.fr")


def test_new_detinataires_payload_invalide(client):
    r = client.post("/new-detinataires", json={})
    assert r.status_code == 422


@patch("api.SpamShield_Operations")
def test_delete_destinataire(mock_ops, client):
    r = client.delete("/delete-destinataire/2")
    assert r.status_code == 200
    mock_ops.return_value.Delete_Destinataire.assert_called_once_with(2)


# -- Champs obligatoires --

@patch("api.SpamShield_Operations")
def test_get_champs_obligatoire_status(mock_ops, client):
    mock_ops.return_value.Form_Requirements.return_value = {"name": True, "email": True}
    r = client.get("/get-champs-obligatoires-status")
    assert r.status_code == 200
    assert r.json()["form_requirements"]["email"] is True


@patch("api.SpamShield_Operations")
def test_update_champs_obligatoire_status(mock_ops, client):
    r = client.put("/update-champs-obligatoires-status/email")
    assert r.status_code == 200
    mock_ops.return_value.Update_Form_Requirements.assert_called_once_with("email")


# -- Modele IA --

@patch("api.SpamShield_Operations")
def test_get_ai_model_infos(mock_ops, client):
    mock_ops.return_value.Current_Model_Metrics.return_value = {"accuracy": 0.94}
    r = client.get("/get-ai-model-infos")
    assert r.status_code == 200
    assert r.json()["spamshield_infos"]["accuracy"] == 0.94


@patch("api.SpamShield_Operations")
def test_build_virgin_model(mock_ops, client):
    r = client.get("/build_virgin_model")
    assert r.status_code == 200
    mock_ops.return_value.virgin_model.assert_called_once()


@patch("api.SpamShield_Operations")
def test_build_virgin_model_erreur(mock_ops, client):
    mock_ops.return_value.virgin_model.side_effect = Exception("Reinit impossible")
    r = client.get("/build_virgin_model")
    assert r.status_code == 500


# -- Rapport LLM (route critique + incident Mistral) --

@patch("api.SpamShield_Operations")
def test_llm_report(mock_ops, client):
    mock_ops.return_value.llm_report.return_value = {
        "model_used": "mistral-small-2603",
        "llm_response": "Rapport de test.",
    }

    r = client.get("/llm-report")

    assert r.status_code == 200
    assert r.json()["model_used"] == "mistral-small-2603"

    mock_ops.return_value.llm_report.assert_called_once()

@patch("api.SpamShield_Operations")
def test_llm_report_cle_mistral_expiree(mock_ops, client):
    mock_ops.return_value.llm_report.side_effect = Exception(
        "API error: Status 401. Your API key expired."
    )

    r = client.get("/llm-report")

    assert r.status_code == 500
    assert "expired" in r.json()["detail"]