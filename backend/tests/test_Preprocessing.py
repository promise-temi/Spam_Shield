import os
import re
import re
import sys
import pytest
import pandas as pd
import numpy as np
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Preprocessing import Preprocessing
from NLP_Feat_Eng import NLP_Feat_Eng

test_artifact_path = f"{os.path.dirname(__file__)}/data"

df_message_pred = pd.DataFrame([{"text": "bonjour, je suis le nouveau test. J'ai render-vous le lundi qui vient, c'est le meilleur jour de ma vie. la chance haha! il peut me contacter a l'adresse jane.doe@test.com"}])
nlp_feat_eng_message_pred = NLP_Feat_Eng(df_message_pred)
df_result_feat_eng_message_pred = nlp_feat_eng_message_pred.feature_engineering_full_pipeline(update_corpus=False)

def test_set_nltk_french_stop_words():
    prepro = Preprocessing(df_result_feat_eng_message_pred, test_artifact_path)

    assert hasattr(prepro, "stemmer")
    assert hasattr(prepro, "stop_words")
    assert isinstance(prepro.stop_words, set)

    assert "le" in prepro.stop_words
    assert "la" in prepro.stop_words
    assert "de" in prepro.stop_words


def test_remove_stopwords_keeps_tokens():
    prepro = Preprocessing(df_result_feat_eng_message_pred, test_artifact_path)

    
    prepro.df["text_preprocessed"] = prepro.df['text_final']
    prepro.clean_stopwords()
    logging.info(prepro.df["text_preprocessed"].iloc[0])
    result = prepro.df["text_preprocessed"].iloc[0]

    assert "[EMAIL]" in result
    assert "[GREETING]" in result
    assert "test" in result
    assert "[PRONOUN]" not in result
    assert " suis " not in result
    assert " le " not in result


def test_remove_stopwords_keeps_tokens():
    prepro = Preprocessing(df_result_feat_eng_message_pred, test_artifact_path)

    prepro.df["text_preprocessed"] = prepro.df['text_final']
    prepro.clean_stopwords()
    logging.info(prepro.df["text_preprocessed"].iloc[0])
    result = prepro.df["text_preprocessed"].iloc[0]

    assert "[EMAIL]" in result
    assert "[GREETING]" in result
    assert "test" in result
    assert "[PRONOUN]" not in result
    assert " suis " not in result
    assert " le " not in result



def test_apply_stemming():
    df = pd.DataFrame([{
        "text_preprocessed": "immédiatement informations [EMAIL]"
    }])

    prepro = Preprocessing(df, test_artifact_path)
    prepro.apply_stemming()

    result = prepro.df.iloc[0]["text_preprocessed"]

    assert "[EMAIL]" in result
    assert result != "immédiatement informations [EMAIL]"


def test_normalize_tokens():
    df = pd.DataFrame([{"text_preprocessed": "test"}])

    prepro = Preprocessing(df, test_artifact_path)

    result = prepro.normalize_tokens("[email] [money] [Phone]")

    assert result == "[EMAIL] [MONEY] [PHONE]"


def test_space_tokens():
    df = pd.DataFrame([{"text_preprocessed": "test"}])

    prepro = Preprocessing(df, test_artifact_path)

    result = prepro.space_tokens("bonjour[EMAIL]merci[MONEY]")

    assert result == "bonjour [EMAIL] merci [MONEY]"



def test_normalize_and_space_tokens():
    df = pd.DataFrame([{
        "text_preprocessed": "bonjour[email]merci[money]"
    }])

    prepro = Preprocessing(df, test_artifact_path)

    prepro.normalize_and_space_tokens()

    result = prepro.df.iloc[0]["text_preprocessed"]

    assert result == "bonjour [EMAIL] merci [MONEY]"


def test_replace_inf_with_zero():
    df = pd.DataFrame({
        "a": [1, np.inf, -np.inf, np.nan]
    })

    prepro = Preprocessing(df, test_artifact_path)

    prepro.relace_inf_with_zero()

    assert prepro.df["a"].tolist() == [1, 0, 0, 0]


def test_drop_duplicates():
    df = pd.DataFrame({
        "text_preprocessed": [
            "bonjour",
            "bonjour",
            "salut"
        ]
    })

    prepro = Preprocessing(df, test_artifact_path)

    prepro.drop_duplicates_()

    assert len(prepro.df) == 2
    assert prepro.df["text_preprocessed"].tolist() == [
        "bonjour",
        "salut"
    ]



def test_delete_memory_data_existing_file(monkeypatch):
    artifact_path = "fake/path"
    memory_path = f"{artifact_path}/memory_df.parquet"

    removed = {"path": None}

    monkeypatch.setattr(os.path, "exists", lambda path: True)

    def fake_remove(path):
        removed["path"] = path

    monkeypatch.setattr(os, "remove", fake_remove)

    df = pd.DataFrame([{"text_preprocessed": "bonjour"}])
    prepro = Preprocessing(df, artifact_path)

    prepro.delete_memory_data()

    assert removed["path"] == memory_path


def test_memory_data_prediction_pipe():
    df = pd.DataFrame([{
        "text_preprocessed": "bonjour",
        "label": 1
    }])

    prepro = Preprocessing(df, test_artifact_path, prediction_pipe=True)

    prepro.memory_data()

    assert prepro.df_memory.equals(df)



