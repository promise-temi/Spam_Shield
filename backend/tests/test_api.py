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