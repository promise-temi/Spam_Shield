import os
import json
import pandas as pd
import pytest

from unittest.mock import patch, MagicMock


# ============================================================
# HELPERS DE TEST
# ============================================================

def patch_test_database(
    test_db,
    monkeypatch
):
    """
    Force les différents modules de SpamShield
    à utiliser la vraie base de données de test.
    """

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    monkeypatch.setattr(
        "modules.Business_Rules.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    monkeypatch.setattr(
        "Business_Rules.Postgres_DB",
        lambda *args, **kwargs: test_db
    )

    monkeypatch.setattr(
        "modules.Mail_Operations.Postgres_DB",
        lambda *args, **kwargs: test_db
    )


def get_test_message():
    return pd.DataFrame(
        [
            {
                "text": "je suis un test"
            }
        ]
    )


def get_test_metadata():
    return {
        "name": "Jane",
        "surname": "Doe",
        "email": "Jane.Doe@email.com",
        "phone": "0605678978",
        "subject": "Ceci est un test",
        "form_id": "test"
    }


def create_real_test_message(
    spamshield,
    test_db,
    test_model_pred,
    monkeypatch
):
    """
    Crée réellement un message dans la DB de test
    via SpamShield.New_Message().
    """

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda **kwargs: test_model_pred
    )

    patch_test_database(
        test_db,
        monkeypatch
    )

    # Empêche seulement l'envoi réel d'un email
    mock_mail = MagicMock()

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Mail_Operations",
        lambda: mock_mail
    )

    message = get_test_message()
    metadata = get_test_metadata()

    messages_avant = spamshield.Show_Messages(
        "date",
        "tous"
    )

    ids_avant = {
        row["id"]
        for row in messages_avant
    }

    spamshield.New_Message(
        message,
        metadata
    )

    messages_apres = spamshield.Show_Messages(
        "date",
        "tous"
    )

    nouveaux_messages = [
        row
        for row in messages_apres
        if row["id"] not in ids_avant
    ]

    assert len(nouveaux_messages) == 1, (
        "New_Message doit créer exactement "
        "un nouveau message dans la DB de test."
    )

    return nouveaux_messages[0]


# ============================================================
# TEST VIRGIN MODEL
# ============================================================

def test_virgin_model(
    spamshield,
    test_model,
    mock_monitor,
    monkeypatch,
):
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda: test_model
    )

    with patch("modules.Model.mlflow.start_run"), \
         patch("modules.Model.ML_Flow_Operations"), \
         patch("Preprocessing.ML_Flow_Operations"), \
         patch("mlflow.log_artifact"), \
         patch("mlflow.log_metric"), \
         patch("mlflow.sklearn.log_model"):

        spamshield.virgin_model()

    assert os.path.exists(
        "backend/tests/test_ressources/model.pkl"
    )

    assert os.path.exists(
        "backend/tests/test_ressources/tfidf.pkl"
    )

    assert os.path.exists(
        "backend/tests/test_ressources/svd.pkl"
    )

    assert os.path.exists(
        "backend/tests/test_ressources/pca.pkl"
    )

    assert os.path.exists(
        "backend/tests/test_ressources/robust_scaler.pkl"
    )


# ============================================================
# TEST NEW MESSAGE
# ============================================================

def test_new_message(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    nouveau_message = create_real_test_message(
        spamshield,
        test_db,
        test_model_pred,
        monkeypatch
    )

    assert nouveau_message is not None

    assert "id" in nouveau_message

    assert "final_label" in nouveau_message

    assert nouveau_message["final_label"] in [
        True,
        False,
        0,
        1
    ]





# ============================================================
# RETRAIN ALL MESSAGES
# ============================================================

def test_retrain_all_messages(
    spamshield,
    test_model,
    mock_monitor,
    monkeypatch,
):
    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda **kwargs: test_model
    )

    with patch("modules.Model.mlflow.start_run"), \
         patch("modules.Model.ML_Flow_Operations"), \
         patch("Preprocessing.ML_Flow_Operations"), \
         patch("mlflow.log_artifact"), \
         patch("mlflow.log_metric"), \
         patch("mlflow.sklearn.log_model"):

        spamshield.Retrain_All_Messages()


# ============================================================
# UPDATE LABEL
# ============================================================

def test_update_label(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    nouveau_message = create_real_test_message(
        spamshield,
        test_db,
        test_model_pred,
        monkeypatch
    )

    message_id = nouveau_message["id"]

    label_avant = nouveau_message[
        "final_label"
    ]

    spamshield.Update_label(
        message_id
    )

    message_apres = spamshield.Select_Message(
        message_id
    )

    assert message_apres is not None

    assert (
        message_apres["final_label"]
        != label_avant
    )


# ============================================================
# SELECT MESSAGE
# ============================================================

def test_select_message(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    nouveau_message = create_real_test_message(
        spamshield,
        test_db,
        test_model_pred,
        monkeypatch
    )

    message_id = nouveau_message["id"]

    selected_message = spamshield.Select_Message(
        message_id
    )

    assert selected_message is not None

    assert (
        selected_message["id"]
        == message_id
    )


# ============================================================
# SHOW MESSAGES
# ============================================================

def test_show_messages(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    create_real_test_message(
        spamshield,
        test_db,
        test_model_pred,
        monkeypatch
    )

    messages = spamshield.Show_Messages(
        "date",
        "tous"
    )

    assert isinstance(
        messages,
        list
    )

    assert len(messages) > 0


# ============================================================
# REGEX
# ============================================================

def test_add_regex_rule(
    spamshield
):
    pattern_test = (
        "crypto.*gratuit.*test"
    )

    spamshield.Add_Regex_Rule(
        pattern_test
    )

    regexes = (
        spamshield
        .Get_All_Regex_Rules()
    )

    patterns = [
        regex["pattern"]
        if isinstance(regex, dict)
        else regex
        for regex in regexes
    ]

    assert (
        pattern_test
        in patterns
    )


def test_get_all_regex_rules(
    spamshield
):
    result = (
        spamshield
        .Get_All_Regex_Rules()
    )

    assert isinstance(
        result,
        list
    )


def test_delete_regex_rule(
    spamshield
):
    pattern_test = (
        "pattern-a-supprimer"
    )

    spamshield.Add_Regex_Rule(
        pattern_test
    )

    regexes = (
        spamshield
        .Get_All_Regex_Rules()
    )

    regex_a_supprimer = next(
        regex
        for regex in regexes
        if regex["pattern"] == pattern_test
    )

    spamshield.Delete_Regex_Rule(
        regex_a_supprimer["id"]
    )

    regexes_apres = (
        spamshield
        .Get_All_Regex_Rules()
    )

    patterns_apres = [
        regex["pattern"]
        for regex in regexes_apres
    ]

    assert (
        pattern_test
        not in patterns_apres
    )


# ============================================================
# DESTINATAIRES
# ============================================================

def test_get_all_destinataires(
    spamshield
):
    result = (
        spamshield
        .Get_All_Destinataires()
    )

    assert isinstance(
        result,
        list
    )


def test_add_destinataire(
    spamshield
):
    email_test = (
        "nouveau-test@spamshield.fr"
    )

    spamshield.Add_Destinataire(
        email_test
    )

    destinataires = (
        spamshield
        .Get_All_Destinataires()
    )

    emails = [
        destinataire["email"]
        if isinstance(destinataire, dict)
        else destinataire
        for destinataire in destinataires
    ]

    assert (
        email_test
        in emails
    )


def test_delete_destinataire(
    spamshield
):
    email_test = (
        "a-supprimer@spamshield.fr"
    )

    spamshield.Add_Destinataire(
        email_test
    )

    destinataires = (
        spamshield
        .Get_All_Destinataires()
    )

    destinataire_a_supprimer = next(
        destinataire
        for destinataire in destinataires
        if destinataire["email"]
        == email_test
    )

    spamshield.Delete_Destinataire(
        destinataire_a_supprimer["id"]
    )

    destinataires_apres = (
        spamshield
        .Get_All_Destinataires()
    )

    emails_apres = [
        destinataire["email"]
        for destinataire
        in destinataires_apres
    ]

    assert (
        email_test
        not in emails_apres
    )


# ============================================================
# DASHBOARD
# ============================================================

def test_dashboard(
    spamshield,
    test_db,
    test_model_pred,
    mock_monitor,
    monkeypatch,
):
    # Important :
    # on crée réellement un message avant
    # d'appeler le dashboard pour éviter
    # une DB totalement vide.
    create_real_test_message(
        spamshield,
        test_db,
        test_model_pred,
        monkeypatch
    )

    result = spamshield.Dashbord()

    assert result is not None

    assert isinstance(
        result,
        dict
    )


# ============================================================
# REQUIRED METADATA
# ============================================================

@pytest.fixture
def fake_required_metadata(
    tmp_path
):
    contenu = {
        "name": False,
        "surname": False,
        "email": True,
        "phone": False,
        "subject": False,
        "gibberish": False
    }

    fichier = (
        tmp_path
        / "required_metadata.json"
    )

    fichier.write_text(
        json.dumps(contenu)
    )

    return str(fichier)


def test_form_requirements(
    spamshield,
    fake_required_metadata,
    monkeypatch
):
    import builtins

    real_open = builtins.open

    def fake_open(
        file,
        *args,
        **kwargs
    ):
        if str(file).endswith(
            "required_metadata.json"
        ):
            return real_open(
                fake_required_metadata,
                *args,
                **kwargs
            )

        return real_open(
            file,
            *args,
            **kwargs
        )

    monkeypatch.setattr(
        "builtins.open",
        fake_open
    )

    result = (
        spamshield
        .Form_Requirements()
    )

    assert (
        result["email"]
        is True
    )

    assert (
        result["name"]
        is False
    )

    assert (
        result["gibberish"]
        is False
    )


def test_update_form_requirements(
    spamshield,
    fake_required_metadata
):
    spamshield.Update_Form_Requirements(
        "email",
        fake_required_metadata
    )

    with open(
        fake_required_metadata
    ) as file:
        data = json.load(file)

    assert (
        data["email"]
        is False
    )