# import os
# import re
# import re
# import sys
# import pytest
# import pandas as pd

# BASE_DIR = os.path.dirname(__file__)  
# FILE_PATH = os.path.join(BASE_DIR, "test_ressources", "spam_ham_dataset.parquet")



# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
# from NLP_Feat_Eng import NLP_Feat_Eng








# def test_feature_engineering_pipeline():
#     df_messages = pd.read_parquet(FILE_PATH)
#     nfe = NLP_Feat_Eng(df_messages)
#     nfe.feature_engineering_full_pipeline()
#     assert "msg_length" in nfe.df.columns
#     assert "msg_word_count" in nfe.df.columns
#     assert "msg_declarative_sentence_count" in nfe.df.columns
#     assert "msg_interrogative_sentence_count" in nfe.df.columns
#     assert "msg_elliptical_sentence_count" in nfe.df.columns
#     assert "msg_emphatic_exclamation_sentence_count" in nfe.df.columns
#     assert "msg_emphatic_question_sentence_count" in nfe.df.columns
#     assert "coma_count" in nfe.df.columns
#     assert "average_word_length" in nfe.df.columns
#     assert "median_word_length" in nfe.df.columns
#     assert "uppercase_count" in nfe.df.columns
#     assert "lowercase_count" in nfe.df.columns
#     assert "uppercase_ratio" in nfe.df.columns
#     assert "digit_count" in nfe.df.columns
#     assert "word_digit_count" in nfe.df.columns
#     assert "money_count" in nfe.df.columns
#     assert "money_words_count" in nfe.df.columns
#     assert "phone_number_count" in nfe.df.columns
#     assert "email_count" in nfe.df.columns    
#     assert "company_email_count" in nfe.df.columns
#     assert "contact_email_count" in nfe.df.columns
#     assert "support_email_count" in nfe.df.columns
#     assert "noreply_email_count" in nfe.df.columns
#     assert "suspect_email_count" in nfe.df.columns
#     assert "special_character_count" in nfe.df.columns
#     assert "line_break_count" in nfe.df.columns
#     assert "tab_count" in nfe.df.columns
#     assert "emoji_count" in nfe.df.columns
#     assert "whitespace_count" in nfe.df.columns
#     assert "special_character_ratio" in nfe.df.columns
#     assert "text_lower" in nfe.df.columns
#     assert "urgency_word_count" in nfe.df.columns
#     assert "financial_word_count" in nfe.df.columns
#     assert "threat_word_count" in nfe.df.columns
#     assert "authority_word_count" in nfe.df.columns
#     assert "reward_word_count" in nfe.df.columns
#     assert "url_count" in nfe.df.columns
#     assert "suspicious_url_count" in nfe.df.columns
#     assert "shortened_url_count" in nfe.df.columns
#     assert "je_count" in nfe.df.columns
#     assert "tu_count" in nfe.df.columns
#     assert "il_elle_count" in nfe.df.columns
#     assert "nous_count" in nfe.df.columns
#     assert "vous_count" in nfe.df.columns
#     assert "ils_elles_count" in nfe.df.columns
#     assert "on_count" in nfe.df.columns
#     assert "has_greeting" in nfe.df.columns
#     assert "has_politeness" in nfe.df.columns
#     assert "has_signature" in nfe.df.columns
#     assert "text_transformed" in nfe.df.columns
#     assert "text_lower" in nfe.df.columns
#     assert "text" in nfe.df.columns
#     assert "text_final" in nfe.df.columns
#     assert "label" in nfe.df.columns


#     assert df_messages.shape[0] == nfe.df.shape[0]
#     print(nfe.df.head(1))
    
    
    