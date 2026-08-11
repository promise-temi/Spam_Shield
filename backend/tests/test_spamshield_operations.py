import os 

def test_virgin_model(
    spamshield,
    test_model,
    mock_monitor,
    monkeypatch,
):

    # Forcer SpamShield_Operations à utiliser le modèle de test
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda: test_model
    )

    # Neutraliser complètement MLflow
    monkeypatch.setattr(
        "ML_Flow._ensure_mlflow_configured",
        lambda: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.log_artifact",
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.log_metric",
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.sklearn.log_model",
        lambda *args, **kwargs: None
    )

    spamshield.virgin_model()

    mock_monitor.record_methode_result.assert_called_once()

    # Vérifie que les artefacts ont bien été créés
    assert os.path.exists("backend/tests/test_ressources/model.pkl")
    assert os.path.exists("backend/tests/test_ressources/tfidf.pkl")
    assert os.path.exists("backend/tests/test_ressources/svd.pkl")
    assert os.path.exists("backend/tests/test_ressources/pca.pkl")
    assert os.path.exists("backend/tests/test_ressources/robust_scaler.pkl")


data_message = {'text':'je suis un test'}

def test_new_message(
    spamshield,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):

    # Forcer SpamShield_Operations à utiliser le modèle de test
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda: test_model_pred
    )

    # Neutraliser complètement MLflow
    monkeypatch.setattr(
        "ML_Flow._ensure_mlflow_configured",
        lambda: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.log_artifact",
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.log_metric",
        lambda *args, **kwargs: None
    )

    monkeypatch.setattr(
        "ML_Flow.mlflow.sklearn.log_model",
        lambda *args, **kwargs: None
    )


    
    spamshield.New_Message(data_message, '')

    mock_monitor.record_methode_result.assert_called_once()

    # # Vérifie que les artefacts ont bien été créés
    # assert os.path.exists("backend/tests/test_ressources/model.pkl")
    # assert os.path.exists("backend/tests/test_ressources/tfidf.pkl")
    # assert os.path.exists("backend/tests/test_ressources/svd.pkl")
    # assert os.path.exists("backend/tests/test_ressources/pca.pkl")
    # assert os.path.exists("backend/tests/test_ressources/robust_scaler.pkl")

