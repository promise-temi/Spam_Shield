import os
import pandas as pd

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

    # 1. Le monitoring a bien enregistré un succès
    mock_monitor.record_methode_result.assert_called_once_with(
        pipe_type="Spamshield Operations",
        is_success=True,
        name="Virgin Model Training",
        status="success"
    )

    # 2. Les artefacts ont bien été créés
    assert os.path.exists("backend/tests/test_ressources/model.pkl")
    assert os.path.exists("backend/tests/test_ressources/tfidf.pkl")
    assert os.path.exists("backend/tests/test_ressources/svd.pkl")
    assert os.path.exists("backend/tests/test_ressources/pca.pkl")
    assert os.path.exists("backend/tests/test_ressources/robust_scaler.pkl")



from unittest.mock import MagicMock
def test_new_message(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    # Forcer SpamShield_Operations à utiliser le modèle de test
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda **kwargs: test_model_pred
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

    message = pd.DataFrame([{'text': 'je suis un test'}])
    metadata = {
        'name': 'Jane',
        'surname': 'Doe',
        'email': 'Jane.Doe@email.com',
        'phone': '0605678978',
        'subject': 'Ceci est un test',
        'form_id': 'test'
    }

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    monkeypatch.setattr(
    "Business_Rules.Postgres_DB",
    lambda *args, **kwargs: test_db
    )
    

    monkeypatch.setattr(
        "modules.Business_Rules.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    monkeypatch.setattr(
        "modules.Mail_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    mock_mail = MagicMock()
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Mail_Operations",
        lambda: mock_mail
    )
    

    spamshield.New_Message(message, metadata)

    # 1. Le monitoring a été appelé
    mock_monitor.record_methode_result.assert_called()

    
    call_kwargs = mock_monitor.record_prediction.call_args.kwargs
    assert call_kwargs['final_label'] in [0, 1]
    assert isinstance(call_kwargs['confidence_score'], float)
    assert 0.0 <= call_kwargs['confidence_score'] <= 1.0

    # 3. record_banned_patterns appelé
    mock_monitor.record_banned_patterns.assert_called_once()

    # 4. record_gibberish appelé
    mock_monitor.record_gibberish.assert_called_once()


def test_check_model_existence_avec_modele(
    spamshield,
    mock_monitor,
    monkeypatch,
):
    """Un modèle existe déjà dans MLflow → aucun réentraînement déclenché."""

    # Mock ML_Flow_Operations pour simuler un modèle existant
    class _FakeMLFlowOps:
        def get_latest_model(self):
            return "modele_existant"  # ← n'importe quoi de non-None

    monkeypatch.setattr(
        "modules.SpamShield_Operations.ML_Flow_Operations",
        lambda: _FakeMLFlowOps()
    )

    # virgin_model ne doit PAS être appelé
    appels = {"virgin": False}
    monkeypatch.setattr(
        spamshield, "virgin_model",
        lambda: appels.__setitem__("virgin", True)
    )

    spamshield.check_model_existence()

    assert appels["virgin"] is False  # pas de réentraînement
    mock_monitor.record_methode_result.assert_called()


def test_check_model_existence_sans_modele(
    spamshield,
    mock_monitor,
    monkeypatch,
):
    """Aucun modèle dans MLflow → virgin_model est déclenché automatiquement."""

    # Mock ML_Flow_Operations pour simuler l'absence de modèle
    class _FakeMLFlowOps:
        def get_latest_model(self):
            return None  # ← aucun modèle

    monkeypatch.setattr(
        "modules.SpamShield_Operations.ML_Flow_Operations",
        lambda: _FakeMLFlowOps()
    )

    appels = {"virgin": False}
    monkeypatch.setattr(
        spamshield, "virgin_model",
        lambda: appels.__setitem__("virgin", True)
    )

    spamshield.check_model_existence()

    assert appels["virgin"] is True  # réentraînement déclenché
    mock_monitor.record_methode_result.assert_called()








def test_retrain_all_messages(
    spamshield,
    test_model,
    mock_monitor,
    monkeypatch,
):
    """Le réentraînement récupère les messages et relance le pipeline."""

    # Forcer SpamShield_Operations à utiliser le modèle de test
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda **kwargs: test_model
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

    spamshield.Retrain_All_Messages()

    mock_monitor.record_methode_result.assert_called()








def test_update_label(spamshield, mock_monitor):
    """La correction d'un label bascule bien is_corected et final_label en base."""
    # On récupère un message existant pour avoir un ID valide
    messages = spamshield.Show_Messages("date", "tous")
    assert len(messages) > 0, "La base de test doit contenir au moins un message"

    premier_id = messages[0]["id"]
    label_avant = messages[0]["final_label"]

    spamshield.Update_label(premier_id)

    # Le label a bien été inversé en base
    message_apres = spamshield.Select_Message(premier_id)
    assert message_apres["final_label"] != label_avant  # le label a basculé
    mock_monitor.record_methode_result.assert_called()


def test_add_regex_rule(spamshield):
    """Ajout d'une règle regex — elle apparaît dans la liste après ajout."""
    pattern_test = "crypto.*gratuit.*test"

    spamshield.Add_Regex_Rule(pattern_test)

    regexes = spamshield.Get_All_Regex_Rules()
    patterns = [r["pattern"] if isinstance(r, dict) else r for r in regexes]
    assert pattern_test in patterns  # la regex a bien été ajoutée


def test_get_all_regex_rules(spamshield):
    """Récupération de toutes les règles regex — retourne une liste."""
    result = spamshield.Get_All_Regex_Rules()
    assert isinstance(result, list)  # contrat : c'est une liste


def test_delete_regex_rule(spamshield):
    """Suppression d'une règle regex — elle disparaît de la liste."""
    # On ajoute d'abord une regex à supprimer
    pattern_test = "pattern-a-supprimer"
    spamshield.Add_Regex_Rule(pattern_test)

    regexes = spamshield.Get_All_Regex_Rules()
    # On récupère l'id de la regex qu'on vient d'ajouter
    regex_a_suppr = next(r for r in regexes if r["pattern"] == pattern_test)

    spamshield.Delete_Regex_Rule(regex_a_suppr["id"])

    regexes_apres = spamshield.Get_All_Regex_Rules()
    patterns_apres = [r["pattern"] for r in regexes_apres]
    assert pattern_test not in patterns_apres  # la regex a bien été supprimée


def test_get_all_destinataires(spamshield):
    """Récupération de tous les destinataires — retourne une liste."""
    result = spamshield.Get_All_Destinataires()
    assert isinstance(result, list)


def test_add_destinataire(spamshield):
    """Ajout d'un destinataire — il apparaît dans la liste après ajout."""
    email_test = "nouveau-test@spamshield.fr"

    spamshield.Add_Destinataire(email_test)

    destinataires = spamshield.Get_All_Destinataires()
    emails = [d["email"] if isinstance(d, dict) else d for d in destinataires]
    assert email_test in emails


def test_delete_destinataire(spamshield):
    """Suppression d'un destinataire — il disparaît de la liste."""
    email_test = "a-supprimer@spamshield.fr"
    spamshield.Add_Destinataire(email_test)

    destinataires = spamshield.Get_All_Destinataires()
    dest_a_suppr = next(d for d in destinataires if d["email"] == email_test)

    spamshield.Delete_Destinataire(dest_a_suppr["id"])

    destinataires_apres = spamshield.Get_All_Destinataires()
    emails_apres = [d["email"] for d in destinataires_apres]
    assert email_test not in emails_apres


def test_dashboard(spamshield):
    """Le tableau de bord retourne bien les métriques attendues."""
    result = spamshield.Dashbord()

    assert isinstance(result, dict)
    



import json
import pytest


@pytest.fixture
def fake_required_metadata(tmp_path):
    """Crée un fichier required_metadata.json temporaire et contrôlé
    pour que les tests soient reproductibles, indépendamment de l'état réel du fichier."""
    contenu = {
        "name": False,
        "surname": False,
        "email": True,
        "phone": False,
        "subject": False,
        "gibberish": False
    }
    fichier = tmp_path / "required_metadata.json"
    fichier.write_text(json.dumps(contenu))
    return str(fichier)

def test_form_requirements(spamshield, fake_required_metadata, monkeypatch):
    """Récupération du statut des champs obligatoires depuis le fichier de config."""
    import builtins
    real_open = builtins.open

    def fake_open(file, *args, **kwargs):
        if str(file).endswith("required_metadata.json"):
            return real_open(fake_required_metadata, *args, **kwargs)
        return real_open(file, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    result = spamshield.Form_Requirements()  # ← sans argument

    assert result["email"] is True
    assert result["name"] is False
    assert result["gibberish"] is False


def test_update_form_requirements(spamshield, fake_required_metadata):
    """Bascule d'un champ obligatoire : email passe de True à False."""
    # Update_Form_Requirements accepte déjà le path en paramètre
    spamshield.Update_Form_Requirements("email", fake_required_metadata)

    # On relit directement le fichier pour vérifier
    import json
    with open(fake_required_metadata) as f:
        data = json.load(f)
    assert data["email"] is False  # le champ a bien basculé