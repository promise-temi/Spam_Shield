import os
import re
import re
import sys
import pytest
import pandas as pd

BASE_DIR = os.path.dirname(__file__)  
FILE_PATH = os.path.join(BASE_DIR, "test_ressources", "spam_ham_dataset.parquet")



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

def test_company_email_count():
    df_message = pd.DataFrame([{"text": "Mon email est john.doe@example.com et dfdfdfd@dhdhdhd@ddhdh,gstsf, mais aussi jane.doe@example.org mais si vous voulez gagner de l'argent, contactez-moi à john.doe@example.xyz, aprèes il y a contact@exemple.com et support@exemple.com? noreply@test.com et noreply@testtwo.com"}])
    nlp_feat_eng = NLP_Feat_Eng(df_message)
    nlp_feat_eng.company_email_count()
    df_result = nlp_feat_eng.df.iloc[0]
    result = df_result['company_email_count']
    assert result == 6

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

# self.special_character_count()
#         self.line_break_count()
#         self.tab_count()

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



# def test_count_psycho_ugency_words():
#     df_message = pd.DataFrame([{"text": "Acheter en URGENCE le nouvel iphone, cest IMPORTANT, vous ne payerez que 2€, paiement rapide et securisé, mais si vous ne le faites pas, l'offre sera suspendue, offre oficielle, vous pouvez gagnez cette offre exceptionelle"}])
#     nlp_feat_eng = NLP_Feat_Eng(df_message)
#     nlp_feat_eng.lower_the_text()
#     nlp_feat_eng.count_psycho_ugency_words()
#     df_result = nlp_feat_eng.df.iloc[0]
#     result = df_result['urgency_word_count']
#     assert result == 34