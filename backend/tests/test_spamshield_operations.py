import os
import json
import pandas as pd
import pytest

from unittest.mock import patch, MagicMock


# ============================================================
# TEST VIRGIN MODEL
# ============================================================

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

    # Neutraliser MLflow pendant l'entraînement
    with patch("modules.Model.mlflow.start_run"), \
         patch("modules.Model.ML_Flow_Operations"), \
         patch("Preprocessing.ML_Flow_Operations"), \
         patch("mlflow.log_artifact"), \
         patch("mlflow.log_metric"), \
         patch("mlflow.sklearn.log_model"):

        spamshield.virgin_model()

    # Artefacts créés localement
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
    # ========================================================
    # MODEL DE TEST
    # ========================================================

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Model",
        lambda **kwargs: test_model_pred
    )

    # ========================================================
    # MESSAGE
    # ========================================================

    message = pd.DataFrame(
        [
            {
                "text": "je suis un test"
            }
        ]
    )

    metadata = {
        "name": "Jane",
        "surname": "Doe",
        "email": "Jane.Doe@email.com",
        "phone": "0605678978",
        "subject": "Ceci est un test",
        "form_id": "test"
    }

    # ========================================================
    # DATABASE DE TEST
    # ========================================================

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

    # ========================================================
    # MOCK DE save_message
    # ========================================================

    save_message_mock = MagicMock()

    monkeypatch.setattr(
        test_db,
        "save_message",
        save_message_mock
    )

    # ========================================================
    # MAIL MOCKÉ
    # ========================================================

    mock_mail = MagicMock()

    monkeypatch.setattr(
        "modules.SpamShield_Operations.Mail_Operations",
        lambda: mock_mail
    )

    # ========================================================
    # EXECUTION
    # ========================================================

    spamshield.New_Message(
        message,
        metadata
    )

    # ========================================================
    # VERIFICATIONS
    # ========================================================

    # New_Message doit tenter de sauvegarder exactement
    # un message
    save_message_mock.assert_called_once()

    # On récupère tout ce qui a été donné à save_message()
    call_kwargs = save_message_mock.call_args.kwargs

    # --------------------------------------------------------
    # LABEL FINAL
    # --------------------------------------------------------

    assert "final_label" in call_kwargs

    assert call_kwargs["final_label"] in [
        True,
        False
    ]

    # --------------------------------------------------------
    # SCORE DE CONFIANCE
    # --------------------------------------------------------

    assert "model_confidence" in call_kwargs

    assert isinstance(
        call_kwargs["model_confidence"],
        float
    )

    assert (
        0.0
        <= call_kwargs["model_confidence"]
        <= 1.0
    )

    # --------------------------------------------------------
    # TEXTE ORIGINAL
    # --------------------------------------------------------

    assert "raw_text" in call_kwargs

    assert (
        call_kwargs["raw_text"]
        == "je suis un test"
    )

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    assert "metadata" in call_kwargs

    assert (
        call_kwargs["metadata"]
        == metadata
    )

    # --------------------------------------------------------
    # PREDICTION MODEL
    # --------------------------------------------------------

    assert "model_pred" in call_kwargs

    assert isinstance(
        call_kwargs["model_pred"],
        bool
    )

    # --------------------------------------------------------
    # BUSINESS RULES
    # --------------------------------------------------------

    assert "business_rules_label" in call_kwargs

    assert isinstance(
        call_kwargs["business_rules_label"],
        bool
    )

    # --------------------------------------------------------
    # OVERRIDE
    # --------------------------------------------------------

    assert "is_overridden" in call_kwargs

    # --------------------------------------------------------
    # TEXTE PREPROCESSE
    # --------------------------------------------------------

    assert "pred_text" in call_kwargs

    assert isinstance(
        call_kwargs["pred_text"],
        str
    )

    assert len(
        call_kwargs["pred_text"]
    ) > 0

    # --------------------------------------------------------
    # PATTERNS INTERDITS
    # --------------------------------------------------------

    assert "banned_patterns_found" in call_kwargs


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
    mock_monitor
):
    messages = spamshield.Show_Messages(
        "date",
        "tous"
    )

    assert len(messages) > 0, (
        "La base de test doit contenir au moins un message"
    )

    premier_id = messages[0]["id"]

    label_avant = (
        messages[0]["final_label"]
    )

    spamshield.Update_label(
        premier_id
    )

    message_apres = (
        spamshield.Select_Message(
            premier_id
        )
    )

    assert (
        message_apres["final_label"]
        != label_avant
    )


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
        spamshield.Get_All_Regex_Rules()
    )

    patterns = [
        r["pattern"]
        if isinstance(r, dict)
        else r
        for r in regexes
    ]

    assert (
        pattern_test
        in patterns
    )


def test_get_all_regex_rules(
    spamshield
):
    result = (
        spamshield.Get_All_Regex_Rules()
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
        spamshield.Get_All_Regex_Rules()
    )

    regex_a_suppr = next(
        r
        for r in regexes
        if r["pattern"] == pattern_test
    )

    spamshield.Delete_Regex_Rule(
        regex_a_suppr["id"]
    )

    regexes_apres = (
        spamshield
        .Get_All_Regex_Rules()
    )

    patterns_apres = [
        r["pattern"]
        for r in regexes_apres
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
        d["email"]
        if isinstance(d, dict)
        else d
        for d in destinataires
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

    dest_a_suppr = next(
        d
        for d in destinataires
        if d["email"] == email_test
    )

    spamshield.Delete_Destinataire(
        dest_a_suppr["id"]
    )

    destinataires_apres = (
        spamshield
        .Get_All_Destinataires()
    )

    emails_apres = [
        d["email"]
        for d in destinataires_apres
    ]

    assert (
        email_test
        not in emails_apres
    )


# ============================================================
# DASHBOARD
# ============================================================

def test_dashboard(
    spamshield
):
    result = (
        spamshield.Dashbord()
    )

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
    ) as f:
        data = json.load(f)

    assert (
        data["email"]
        is False
    )