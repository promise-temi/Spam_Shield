import os
import re
import re
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from NLP_Feat_Eng import NLP_Feat_Eng



def test_message_length():
    df_message = pd.DataFrame([{"text": "Bonjour, Je suis intéressé par votre produit. Pouvez-vous me donner plus d'informations ? Merci !"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.message_length()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_length']
    assert result == len(df_message.iloc[0]["text"])


def test_word_count():
    df_message = pd.DataFrame([{"text": "Bonjour, Je suis intéressé par votre produit. Pouvez-vous me donner plus d'informations ? Merci !"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.word_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_word_count']
    assert result == len(df_message.iloc[0]["text"].split())


def test_declarative_caracters():
    df_message = pd.DataFrame([{"text": "Bonjour, Je suis intéressé par votre produit. C'est peu commun. Je voudrait plus plus d'informations..."}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_declarative_caracters()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_declarative_sentence_count']
    assert result == 2

def test_interrogative_caracters():
    df_message = pd.DataFrame([{"text": "Bonjour? Vous vendez vous ce produit???? S'il vous plait? Merci pour votre réponse? Vous répondez??"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_interrogative_caracters()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_interrogative_sentence_count']
    assert result == 3

def test_exclamative_caracters():
    df_message = pd.DataFrame([{"text": "Bonjour! J'adore ce que vous faites! S'il vous plait!!!! Merci pour votre réponse! Vous répondez!!"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_exclamative_caracters()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_exclamative_sentence_count']
    assert result == 3

def test_elliptical_caracters():
    df_message = pd.DataFrame([{"text": "Bonjour... Je suis désépéré... S'il vous plait.. Répondez... Merci."}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_elliptical_caracters()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_elliptical_sentence_count']
    assert result == 4

def test_emphatic_exclamations():
    df_message = pd.DataFrame([{"text": "Bonjour! J'adore ce que vous faites! S'il vous plait!!!! Merci pour votre réponse! Vous répondez!!"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_emphatic_exclamations()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_emphatic_exclamation_sentence_count']
    assert result == 2

def test_emphatic_questions():
    df_message = pd.DataFrame([{"text": "Bonjour? Vous vendez vous ce produit???? S'il vous plait? Merci pour votre réponse? Vous répondez??"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_emphatic_questions()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['msg_emphatic_question_sentence_count']
    assert result == 2

def test_commas():
    df_message = pd.DataFrame([{"text": "Bonjour, vous ne me connaissez sans doute pas, mais moi si. Vous produits, services et autres... m'interessent beaucoup. "}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.count_commas()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['coma_count']
    assert result == 3

def test_average_word_length():
    df_message = pd.DataFrame([{"text": "HELLO JE me NOMME Propro"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.average_word_length()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['average_word_length']
    assert result == 4

def test_median_word_length():
    df_message = pd.DataFrame([{"text": "HELLO JE me NOMME Propro"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.median_word_length()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['median_word_length']
    assert result == 5

def test_uppercase_count():
    df_message = pd.DataFrame([{"text": "HELLO JE me NOMME Propro"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.uppercase_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['uppercase_count']
    assert result == 13

def test_lowercase_count():
    df_message = pd.DataFrame([{"text": "HELLO JE me NOMME Propro"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lowercase_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['lowercase_count']
    assert result == 7

def test_uppercase_ratio():
    df_message = pd.DataFrame([{"text": "HELLO JE me NOMME Propro"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lowercase_count()
    nlp_feat_eng.uppercase_count()
    nlp_feat_eng.uppercase_ratio()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['uppercase_ratio']
    assert result == 65

def test_digit_count():
    df_message = pd.DataFrame([{"text": "j'ai 23€ en poche, j'ai bien dit vingt-trois euros! Cela depuis 2009, non 1990"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.digit_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['digit_count']
    assert result == 10

def test_word_digit_count():
    df_message = pd.DataFrame([{"text": "j'ai 23€ en poche, j'ai bien dit vingt-trois euros! Cela depuis 2009, non 1990"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.word_digit_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['word_digit_count']
    assert result == 2

def test_money_count():
    df_message = pd.DataFrame([{"text": "j'ai 23€ en poche, j'ai bien dit vingt-trois euros! Cela depuis 2009, non 1990"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.money_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['money_count']
    assert result == 1

def test_money_words_count():
    df_message = pd.DataFrame([{"text": "j'ai 23€ en poche, j'ai bien dit vingt-trois euros! Cela depuis 2009, non 1990"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.money_words_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['money_words_count']
    assert result == 1

def test_phone_number_count():
    df_message = pd.DataFrame([{"text": "contactez moi au 07 54 27 89 20 ou au 9876564532 ou bien au 09.48.47.76.34"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.phone_number_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['phone_number_count']
    assert result == 2

def test_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['email_count']
    assert result == 7


def test_contact_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.contact_email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['contact_email_count']
    assert result == 1

def test_support_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.support_email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['support_email_count']
    assert result == 1

def test_noreply_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.noreply_email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['noreply_email_count']
    assert result == 2

def test_suspect_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.suspect_email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['suspect_email_count']
    assert result == 1

def test_special_character_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et('-è_-(_)) support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.special_character_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['special_character_count']
    assert result == 35

def test_special_character_ratio():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et('-è_-(_)) support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.message_length()
    nlp_feat_eng.special_character_count()
    nlp_feat_eng.special_character_ratio()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['special_character_ratio']
    assert int(result) == int(36/df_result["msg_length"] * 100)

def test_suspect_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et \ndfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais \nsi vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et \nnoreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.line_break_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['line_break_count']
    assert result == 3

def test_tab_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, \t \tmais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et  \t support@exemple.com?  \t noreply@test.com et \t noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.tab_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['tab_count']
    assert result == 5

def test_whitespace_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, \t \tmais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et  \t support@exemple.com?  \t noreply@test.com et \t noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.whitespace_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['whitespace_count']
    assert result == 34


def test_lower_the_text():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, \t \tmais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et  \t support@exemple.com?  \t noreply@test.com et \t noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    df_result = nlp_feat_eng.df.iloc[0]
    

    df_message2 = pd.DataFrame([{"text":df_result['text_lower']}])
    nlp_feat_eng2 = NLP_Feat_Eng(df_message2)
    nlp_feat_eng2.uppercase_count()
    df_result2 = nlp_feat_eng2.df.iloc[0]
    result = df_result2['uppercase_count']
    assert result == 0

def test_count_psycho_ugency_words():
    df_message = pd.DataFrame([{"text": "Acheter en URGENCE le nouvel iphone, cest IMPORTANT, vous ne payerez que 2€, paiement rapide et securisé, mais si vous ne le faites pas, l'offre sera suspendue, offre oficielle, vous pouvez gagnez cette offre exceptionelle"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_psycho_ugency_words()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['urgency_word_count']
    assert result == 3

def test_count_financial_words():
    df_message = pd.DataFrame([{"text": "Acheter en URGENCE le nouvel iphone, cest IMPORTANT, vous ne payerez que 2€, paiement rapide et securisé, mais si vous ne le faites pas, l'offre sera suspendue, offre oficielle, vous pouvez gagnez cette offre exceptionelle"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_financial_words()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['financial_word_count']
    assert result == 3

def test_count_threat_words():
    df_message = pd.DataFrame([{"text": "Acheter en URGENCE le nouvel iphone, cest IMPORTANT, vous ne payerez que 2€, paiement rapide et securisé, mais si vous ne le faites pas, l'offre sera suspendue, offre oficielle, vous pouvez gagnez cette offre exceptionelle"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_threat_words()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['threat_word_count']
    assert result == 1


def test_count_authority_words():
    df_message = pd.DataFrame([{"text": "selon le gouverNement vous devez Contacter Le SerVice client pour support, message de l'assurance malaDie, pour assIsTance"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_authority_words()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['authority_word_count']
    assert result == 5

def test_count_reward_words():
    df_message = pd.DataFrame([{"text": "Nouvelle promotion, gagner un iphone gratuit, bonus incroyable"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_reward_words()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['reward_word_count']
    assert result == 4


def test_count_urls():
    df_message = pd.DataFrame([{
        "text": "Visitez https://example.com, http://test.fr, http//fake.com, http#//weird.com, http_//strange.com, hxxp://danger.xyz et www.site.com et site_interessant.net"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_urls()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["url_count"]

    assert result == 8


def test_count_suspicious_urls():
    df_message = pd.DataFrame([{
        "text": "Cliquez sur https://arnaque.xyz, www.site.ru, hxxp://danger.top et https://normal.com"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_suspicious_urls()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["suspicious_url_count"]

    assert result == 3


def test_count_shortened_urls():
    df_message = pd.DataFrame([{
        "text": "Va sur bit.ly/test, https://tinyurl.com/abc, www.t.co/link et https://example.com"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_shortened_urls()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["shortened_url_count"]

    assert result == 3


def test_count_personal_pronouns():
    df_message = pd.DataFrame([{
        "text": "Je pense que j'ai raison, tu sais. Il vient, elle aussi. Nous partons, vous restez. Ils arrivent, elles aussi, on verra."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_personal_pronouns()

    df_result = nlp_feat_eng.df.iloc[0]

    assert df_result["je_count"] == 2
    assert df_result["tu_count"] == 1
    assert df_result["il_elle_count"] == 2
    assert df_result["nous_count"] == 1
    assert df_result["vous_count"] == 1
    assert df_result["ils_elles_count"] == 2
    assert df_result["on_count"] == 1


def test_count_negations():
    df_message = pd.DataFrame([{
        "text": "Je ne veux pas venir, n'accepte plus jamais aucune offre, ni aucun message. Rien de tout ça. Promotion, panier, animal."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_negations()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["negation_count"]

    assert result == 9

def test_count_dates():
    df_message = pd.DataFrame([{
        "text": "Rendez-vous le 21/06/2025, puis le 2025-06-22 et enfin le 23 juin 2025. Attention 99/99/9999 est compté aussi par la regex."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_dates()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["date_count"]

    assert result == 4

  


def test_count_temporal_words():
    df_message = pd.DataFrame([{
        "text": "Aujourd'hui demain hier maintenant immédiatement bientôt prochainement autrefois auparavant désormais toujours jamais souvent parfois ensuite puis avant après tôt tard ce matin cet après-midi ce soir cette nuit lundi mardi janvier février promotion maintenant."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_temporal_words()

    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result["temporal_words_count"]

    assert result == 29



def test_count_greetings():
    df_message = pd.DataFrame([{
        "text": "Bonjour Madame, bienvenue ! Promotion, salutation, bonsoirée."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_greetings()

    df_result = nlp_feat_eng.df.iloc[0]

    assert df_result["has_greeting"] == 1


def test_count_politeness():
    df_message = pd.DataFrame([{
        "text": "Merci beaucoup pour votre aide. Je vous remercie. Mercier est mon nom."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_politeness()

    df_result = nlp_feat_eng.df.iloc[0]

    assert df_result["has_politeness"] == 1


def test_count_signatures():
    df_message = pd.DataFrame([{
        "text": "Bien cordialement,\nJean Dupont\nAmicalement vôtre."
    }])

    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.count_signatures()
    df_result = nlp_feat_eng.df.iloc[0]

    assert df_result["has_signature"] == 1

@pytest.fixture
def mock_metadata_business_rules(monkeypatch):
    """Neutralise Metadata_Business_Rules dans NLP_Feat_Eng pour que
    check_name / check_surname renvoient True sans charger de ressources réelles
    (corpus, détecteur de charabia...). On teste ainsi la logique d'anonymisation
    de replace_sensitive_personal_data de façon isolée et reproductible."""
    from unittest.mock import MagicMock

    fake_mbr = MagicMock()
    fake_mbr.check_name.return_value = True
    fake_mbr.check_surname.return_value = True
    fake_mbr.check_email.return_value = True
    fake_mbr.check_phone.return_value = True

    monkeypatch.setattr(
        "modules.NLP_Feat_Eng.Metadata_Business_Rules",
        lambda *args, **kwargs: fake_mbr
    )
    return fake_mbr

import logging

def test_replace_sensitive_personal_data_name(mock_metadata_business_rules):  # ← ajout
    metadata = {"name":"Jane"}
    df_message = pd.DataFrame([{"text": "Bonjour, je m'appelle Jane Doe! oui jane dOe"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message, metadata=metadata)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_sensitive_personal_data()
    df_result = nlp_feat_eng.df.iloc[0]
    assert df_result['text_transformed'].count('[SENSITIVE]') == 2
    logging.info(df_result['text_transformed'])


def test_replace_sensitive_personal_data_surname(mock_metadata_business_rules):  # ← ajout
    metadata = {"surname":"DOE"}
    df_message = pd.DataFrame([{"text": "Bonjour, je m'appelle Jane Doe! oui jane dOe"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message, metadata=metadata)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_sensitive_personal_data()
    df_result = nlp_feat_eng.df.iloc[0]
    assert df_result['text_transformed'].count('[SENSITIVE]') == 2
    logging.info(df_result['text_transformed'])


def test_replace_sensitive_personal_data(mock_metadata_business_rules):  # ← ajout
    metadata = {"name":"JanE", "surname":"DOE"}
    df_message = pd.DataFrame([{"text": "Bonjour, je m'appelle Jane Doe! oui jane dOe"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message, metadata=metadata)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_sensitive_personal_data()
    df_result = nlp_feat_eng.df.iloc[0]
    assert df_result['text_transformed'].count('[SENSITIVE]') == 4
    logging.info(df_result['text_transformed'])


def test_replace_sensitive_personal_data_none_specified(mock_metadata_business_rules):  # ← ajout
    metadata = {"name":"","surname":"","email":""}
    df_message = pd.DataFrame([{"text": "Bonjour, je m'appelle Jane Doe! oui jane dOe"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message, metadata=metadata)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_sensitive_personal_data()
    df_result = nlp_feat_eng.df.iloc[0]
    assert df_result['text_transformed'].count('[SENSITIVE]') == 0
    logging.info(df_result['text_transformed'])



def test_replace_money_info():
    df_message = pd.DataFrame([{
        "text": "Payez 150€, 20 euros, 30 dollars et 999€ maintenant. Code promo."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_money_info()
    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[MONEY]" in result
    assert result.count("[MONEY]") == 4


def test_replace_phone_info():
    df_message = pd.DataFrame([{
        "text": "Appelez le 0612345678 ou 06 12 34 56 78 ou +33 6 12 34 56 78. Code 1234."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_phone_info()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[PHONE]" in result
    assert result.count("[PHONE]") == 2


def test_replace_email_info():
    df_message = pd.DataFrame([{
        "text": "Contactez contact@entreprise.com, noreply@site.com, test@gmail.com et support@corp.fr"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_email_info()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[EMAIL]" in result
    assert result.count("[EMAIL]") == 4


def test_replace_psycho_urgency_words():
    df_message = pd.DataFrame([{
        "text": "Urgent, votre compte bancaire sera bloqué par le gouvernement. Gagnez un bonus gratuit."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_psycho_urgency_words()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[URGENCY]" in result
    assert "[FINANCIAL]" in result
    assert "[THREAT]" in result
    assert "[AUTHORITY]" in result
    assert "[REWARD]" in result


def test_replace_urls():
    df_message = pd.DataFrame([{
        "text": "Va sur https://danger.xyz, bit.ly/test, https://normal.com et site_interessant.net"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_urls()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[URL]" in result
    assert result.count("[URL]") >= 1

def test_replace_dates():
    df_message = pd.DataFrame([{
        "text": "Rendez-vous le 21/06/2025, le 2025-06-22 et le 23 juin 2025."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    
    nlp_feat_eng.replace_dates()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[DATE]" in result
    assert result.count("[DATE]") == 3


def test_replace_temporal_words():
    df_message = pd.DataFrame([{
        "text": "Aujourd'hui demain hier maintenant ce matin promotion."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    
    nlp_feat_eng.replace_temporal_words()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[TEMPORAL]" in result
    assert result.count("[TEMPORAL]") == 5


def test_replace_digits():
    df_message = pd.DataFrame([{
        "text": "J'ai 2 codes, trois essais et 99 problèmes."
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    
    nlp_feat_eng.replace_digits()

    result = nlp_feat_eng.df.iloc[0]["text_transformed"]

    assert "[DIGIT]" in result
    assert result.count("[DIGIT]") == 4
   


def test_clean_special_characters():
    df_message = pd.DataFrame([{
        "text": "Bonjour!!! J'ai un code-test email@email.com @@@"
    }])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.lower_the_text()
    nlp_feat_eng.replace_email_info()
    
    nlp_feat_eng.clean_special_characters()

    result = nlp_feat_eng.df.iloc[0]["text_final"]

    assert "!" not in result
    assert "@" not in result
    assert "-" not in result
    assert "'" not in result
    assert "[EMAIL]" in result

