import os
import sys
import datetime
import pytest

from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)


os.environ["BACKEND_API_KEY"] = "cle-de-test-1234"
os.environ["ENCRYPTION_KEY"] = "RxdMLSRTwGMYW6gNoAEvlWbdOHI6iDzjssyXCMMzq2I="
os.environ["MISTRAL_API_KEY"] = "cle-mistral-factice-pour-les-tests"
os.environ["EMAIL_ADDRESS"] = "admin@spamshield.test"
os.environ["EMAIL_PASSWORD"] = "mot-de-passe-test"


with patch("mlflow.set_tracking_uri"), patch("mlflow.set_experiment"):
    with patch(
        "modules.SpamShield_Operations.SpamShield_Operations.check_model_existence"
    ):
        from api import (
            app,
            require_api_key,
            require_session
        )


@pytest.fixture
def client():
    app.dependency_overrides[require_api_key] = lambda: None
    app.dependency_overrides[require_session] = lambda: {
        "session_id": 1,
        "email": "admin@spamshield.test"
    }

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def client_auth_active():
    app.dependency_overrides.clear()
    return TestClient(app)


ROUTES_SESSION = [
    ("GET", "/dashboard-metrics", None),
    ("GET", "/get-messages/date/tous", None),
    ("GET", "/get_message-and-related-metrics/1", None),
    ("GET", "/update_label/1", None),
    ("GET", "/get-regexes", None),
    ("POST", "/new-regex", {"pattern": "test"}),
    ("DELETE", "/delete-regex/1", None),
    ("GET", "/get-detinataires", None),
    ("POST", "/new-detinataires", {"destinataire": "test@test.fr"}),
    ("DELETE", "/delete-destinataire/1", None),
    ("GET", "/get-champs-obligatoires-status", None),
    ("PUT", "/update-champs-obligatoires-status/email", None),
    ("GET", "/get-ai-model-infos", None),
    ("GET", "/build_virgin_model", None),
    ("GET", "/retrain_model", None),
    ("GET", "/llm-report", None),
]


@pytest.mark.parametrize(
    "method,url,payload",
    ROUTES_SESSION
)
def test_route_admin_sans_session_refusee(
    client_auth_active,
    method,
    url,
    payload
):
    response = client_auth_active.request(
        method,
        url,
        json=payload
    )

    assert response.status_code == 401


def test_new_message_sans_api_key_refuse(client_auth_active):
    response = client_auth_active.post(
        "/new-message",
        json=PAYLOAD_VALIDE
    )

    assert response.status_code == 422


def test_new_message_api_key_invalide(client_auth_active):
    with patch(
        "api.security.verify_api_key",
        return_value=False
    ):
        response = client_auth_active.post(
            "/new-message",
            json=PAYLOAD_VALIDE,
            headers={
                "x-api-key": "cle-invalide"
            }
        )

    assert response.status_code == 401


def test_request_code_email_non_autorise(client_auth_active):
    response = client_auth_active.post(
        "/auth/request-code",
        json={
            "email": "intrus@test.fr"
        }
    )

    assert response.status_code == 403


def test_request_code_email_autorise(client_auth_active):
    mock_db = MagicMock()
    mock_smtp = MagicMock()

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.generate_login_code",
        return_value="123456"
    ), patch(
        "api.security.hash_value",
        return_value="hash-code"
    ), patch(
        "api.smtplib.SMTP_SSL",
        return_value=mock_smtp
    ):
        mock_smtp.__enter__.return_value = mock_smtp

        response = client_auth_active.post(
            "/auth/request-code",
            json={
                "email": "admin@spamshield.test"
            }
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Code envoyé."

    mock_db.create_auth_code.assert_called_once()

    mock_smtp.login.assert_called_once()
    mock_smtp.send_message.assert_called_once()


def test_verify_code_valide(client_auth_active):
    mock_db = MagicMock()

    mock_db.get_latest_auth_code.return_value = (
        1,
        "hash-code",
        datetime.datetime.now()
        + datetime.timedelta(minutes=5)
    )

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.verify_hashed_value",
        return_value=True
    ), patch(
        "api.security.generate_session_token",
        return_value="session-test"
    ), patch(
        "api.security.hash_value",
        return_value="session-hash"
    ):
        response = client_auth_active.post(
            "/auth/verify-code",
            json={
                "email": "admin@spamshield.test",
                "code": "123456"
            }
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Connexion réussie."

    cookie = response.headers.get("set-cookie")

    assert cookie is not None
    assert "session_token=" in cookie
    assert "HttpOnly" in cookie

    mock_db.activate_auth_session.assert_called_once()


def test_verify_code_invalide(client_auth_active):
    mock_db = MagicMock()

    mock_db.get_latest_auth_code.return_value = (
        1,
        "hash-code",
        datetime.datetime.now()
        + datetime.timedelta(minutes=5)
    )

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.verify_hashed_value",
        return_value=False
    ):
        response = client_auth_active.post(
            "/auth/verify-code",
            json={
                "email": "admin@spamshield.test",
                "code": "999999"
            }
        )

    assert response.status_code == 401


def test_verify_code_expire(client_auth_active):
    mock_db = MagicMock()

    mock_db.get_latest_auth_code.return_value = (
        1,
        "hash-code",
        datetime.datetime.now()
        - datetime.timedelta(minutes=1)
    )

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ):
        response = client_auth_active.post(
            "/auth/verify-code",
            json={
                "email": "admin@spamshield.test",
                "code": "123456"
            }
        )

    assert response.status_code == 401


def test_auth_me_session_valide(client_auth_active):
    mock_db = MagicMock()

    mock_db.get_session_by_token.return_value = (
        1,
        "admin@spamshield.test",
        datetime.datetime.now()
        + datetime.timedelta(hours=1)
    )

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.hash_value",
        return_value="session-hash"
    ):
        response = client_auth_active.get(
            "/auth/me",
            cookies={
                "session_token": "session-test"
            }
        )

    assert response.status_code == 200
    assert response.json()["authenticated"] is True
    assert response.json()["email"] == "admin@spamshield.test"


def test_auth_me_session_invalide(client_auth_active):
    mock_db = MagicMock()
    mock_db.get_session_by_token.return_value = None

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.hash_value",
        return_value="session-hash"
    ):
        response = client_auth_active.get(
            "/auth/me",
            cookies={
                "session_token": "session-invalide"
            }
        )

    assert response.status_code == 401


def test_auth_me_session_expiree(client_auth_active):
    mock_db = MagicMock()

    mock_db.get_session_by_token.return_value = (
        1,
        "admin@spamshield.test",
        datetime.datetime.now()
        - datetime.timedelta(minutes=1)
    )

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.hash_value",
        return_value="session-hash"
    ):
        response = client_auth_active.get(
            "/auth/me",
            cookies={
                "session_token": "session-test"
            }
        )

    assert response.status_code == 401

    mock_db.delete_session.assert_called_once_with(
        "session-hash"
    )


def test_logout(client_auth_active):
    mock_db = MagicMock()

    with patch(
        "api.Postgres_DB",
        return_value=mock_db
    ), patch(
        "api.security.hash_value",
        return_value="session-hash"
    ):
        response = client_auth_active.post(
            "/auth/logout",
            cookies={
                "session_token": "session-test"
            }
        )

    assert response.status_code == 200
    assert response.json()["message"] == "Déconnexion réussie."

    mock_db.delete_session.assert_called_once_with(
        "session-hash"
    )


PAYLOAD_VALIDE = {
    "message": "Bonjour, je souhaite un devis.",
    "metadata": {
        "name": "Dupont",
        "surname": "Jean",
        "email": "jean.dupont@example.com",
        "phone": "0600000000",
        "subject": "Devis",
        "form_id": "contact-1"
    },
    "settings": {
        "entrainementModel": True,
        "recevoirParMail": False
    }
}


@patch("api.SpamShield_Operations")
def test_dashboard_metrics(mock_ops, client):
    mock_ops.return_value.Dashbord.return_value = {
        "messages": 10,
        "spam": 5
    }

    response = client.get(
        "/dashboard-metrics"
    )

    assert response.status_code == 200
    assert response.json()["metrics"] == {
        "messages": 10,
        "spam": 5
    }


@patch("api.SpamShield_Operations")
def test_dashboard_metrics_erreur(mock_ops, client):
    mock_ops.return_value.Dashbord.side_effect = Exception(
        "DB indisponible"
    )

    response = client.get(
        "/dashboard-metrics"
    )

    assert response.status_code == 500


@patch("api.SpamShield_Operations")
def test_get_all_messages(mock_ops, client):
    mock_ops.return_value.Show_Messages.return_value = [
        {
            "id": 1,
            "label": "ham"
        }
    ]

    response = client.get(
        "/get-messages/date/tous"
    )

    assert response.status_code == 200

    assert response.json()["messages"] == [
        {
            "id": 1,
            "label": "ham"
        }
    ]

    mock_ops.return_value.Show_Messages.assert_called_once_with(
        "date",
        "tous"
    )


@patch("api.SpamShield_Operations")
def test_get_message_and_related_metrics(mock_ops, client):
    mock_ops.return_value.Select_Message.return_value = {
        "id": 42
    }

    response = client.get(
        "/get_message-and-related-metrics/42"
    )

    assert response.status_code == 200
    assert response.json()["selected_message"]["id"] == 42

    mock_ops.return_value.Select_Message.assert_called_once_with(
        42
    )


@patch("api.SpamShield_Operations")
def test_update_label(mock_ops, client):
    response = client.get(
        "/update_label/7"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "ok"
    }

    mock_ops.return_value.Update_label.assert_called_once_with(
        7
    )


@patch("api.SpamShield_Operations")
def test_new_message(mock_ops, client):
    response = client.post(
        "/new-message",
        json=PAYLOAD_VALIDE
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "ok"
    }

    mock_ops.return_value.New_Message.assert_called_once()


def test_new_message_payload_invalide(client):
    response = client.post(
        "/new-message",
        json={
            "message": "texte seul"
        }
    )

    assert response.status_code == 422


@patch("api.SpamShield_Operations")
def test_new_message_erreur(mock_ops, client):
    mock_ops.return_value.New_Message.side_effect = Exception(
        "Echec classification"
    )

    response = client.post(
        "/new-message",
        json=PAYLOAD_VALIDE
    )

    assert response.status_code == 500


@patch("api.SpamShield_Operations")
def test_get_regexes(mock_ops, client):
    mock_ops.return_value.Get_All_Regex_Rules.return_value = [
        "casino",
        "viagra"
    ]

    response = client.get(
        "/get-regexes"
    )

    assert response.status_code == 200

    assert response.json()["regex_rules"] == [
        "casino",
        "viagra"
    ]


@patch("api.SpamShield_Operations")
def test_new_regex(mock_ops, client):
    response = client.post(
        "/new-regex",
        json={
            "pattern": "crypto.*gratuit"
        }
    )

    assert response.status_code == 200

    mock_ops.return_value.Add_Regex_Rule.assert_called_once_with(
        "crypto.*gratuit"
    )


def test_new_regex_payload_invalide(client):
    response = client.post(
        "/new-regex",
        json={}
    )

    assert response.status_code == 422


@patch("api.SpamShield_Operations")
def test_delete_regex(mock_ops, client):
    response = client.delete(
        "/delete-regex/3"
    )

    assert response.status_code == 200

    mock_ops.return_value.Delete_Regex_Rule.assert_called_once_with(
        3
    )


@patch("api.SpamShield_Operations")
def test_get_detinataires(mock_ops, client):
    mock_ops.return_value.Get_All_Destinataires.return_value = [
        "contact@spamshield.fr"
    ]

    response = client.get(
        "/get-detinataires"
    )

    assert response.status_code == 200

    assert response.json()["destinataires"] == [
        "contact@spamshield.fr"
    ]


@patch("api.SpamShield_Operations")
def test_new_detinataires(mock_ops, client):
    response = client.post(
        "/new-detinataires",
        json={
            "destinataire": "alerte@spamshield.fr"
        }
    )

    assert response.status_code == 200

    mock_ops.return_value.Add_Destinataire.assert_called_once_with(
        "alerte@spamshield.fr"
    )


def test_new_detinataires_payload_invalide(client):
    response = client.post(
        "/new-detinataires",
        json={}
    )

    assert response.status_code == 422


@patch("api.SpamShield_Operations")
def test_delete_destinataire(mock_ops, client):
    response = client.delete(
        "/delete-destinataire/2"
    )

    assert response.status_code == 200

    mock_ops.return_value.Delete_Destinataire.assert_called_once_with(
        2
    )


@patch("api.SpamShield_Operations")
def test_get_champs_obligatoire_status(mock_ops, client):
    mock_ops.return_value.Form_Requirements.return_value = {
        "name": True,
        "email": True
    }

    response = client.get(
        "/get-champs-obligatoires-status"
    )

    assert response.status_code == 200
    assert response.json()["form_requirements"]["email"] is True


@patch("api.SpamShield_Operations")
def test_update_champs_obligatoire_status(mock_ops, client):
    response = client.put(
        "/update-champs-obligatoires-status/email"
    )

    assert response.status_code == 200

    mock_ops.return_value.Update_Form_Requirements.assert_called_once_with(
        "email"
    )


@patch("api.SpamShield_Operations")
def test_get_ai_model_infos(mock_ops, client):
    mock_ops.return_value.Current_Model_Metrics.return_value = {
        "accuracy": 0.94
    }

    response = client.get(
        "/get-ai-model-infos"
    )

    assert response.status_code == 200
    assert response.json()["spamshield_infos"]["accuracy"] == 0.94


@patch("api.SpamShield_Operations")
def test_build_virgin_model(mock_ops, client):
    response = client.get(
        "/build_virgin_model"
    )

    assert response.status_code == 200

    mock_ops.return_value.virgin_model.assert_called_once()


@patch("api.SpamShield_Operations")
def test_build_virgin_model_erreur(mock_ops, client):
    mock_ops.return_value.virgin_model.side_effect = Exception(
        "Reinit impossible"
    )

    response = client.get(
        "/build_virgin_model"
    )

    assert response.status_code == 500


@patch("api.SpamShield_Operations")
def test_retrain_model(mock_ops, client):
    response = client.get(
        "/retrain_model"
    )

    assert response.status_code == 200

    mock_ops.return_value.Retrain_All_Messages.assert_called_once()


@patch("api.SpamShield_Operations")
def test_llm_report(mock_ops, client):
    mock_ops.return_value.llm_report.return_value = {
        "model_used": "mistral-small-2603",
        "llm_response": "Rapport de test."
    }

    response = client.get(
        "/llm-report"
    )

    assert response.status_code == 200
    assert response.json()["model_used"] == "mistral-small-2603"

    mock_ops.return_value.llm_report.assert_called_once()


@patch("api.SpamShield_Operations")
def test_llm_report_cle_mistral_expiree(mock_ops, client):
    mock_ops.return_value.llm_report.side_effect = Exception(
        "API error: Status 401. Your API key expired."
    )

    response = client.get(
        "/llm-report"
    )

    assert response.status_code == 500
    assert "expired" in response.json()["detail"]