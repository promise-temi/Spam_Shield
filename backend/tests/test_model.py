import os
import re
import re
import sys


# BASE_DIR = os.path.dirname(__file__)  
# FILE_PATH = os.path.join(BASE_DIR, "test_ressources", "spam_ham_dataset.parquet")



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from Model import Model
from Set_SpamShield import SET_Spam_Shield_Dependances








def test_AI_full_virgin_model_training_pipeline():
    df_messages = SET_Spam_Shield_Dependances(raw_data_dir="data/raw_data").Dependances_Full_Pipeline(lang='fr')
    assert type(df_messages) == "<class 'pandas.core.frame.DataFrame'>"
    model_ = Model()
    model_.AI_full_virgin_model_training_pipeline(df_messages)

    # tester que les colonnes numériques ne contiennent pas de données textuelles lors de la phase de train_test_split
    # num_cols = model_.X_num
    # for col in num_cols.columns:
    #     assert not any(model_.X_num[col].apply(lambda x: isinstance(x, str))), f"La colonne {col} contient des données textuelles."

# def test_retrain_model_pipeline():
#     df = pd.DataFrame([
#         {'label': 0, 'text': "Bonjour, je m'intéresse à vos services"},
#         {'label': 1, 'text': "Gagnez de l'argent rapidement en cliquant ici !"},
#         {'label': 0, 'text': "Merci pour votre message. Je vous répondrai bientôt."},
#         {'label': 1, 'text': "Offre spéciale : obtenez 50% de réduction sur tous nos produits !"},
#         {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
#         {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
#         {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
#         {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
#         {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
#         {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."},
#         {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
#         {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
#         {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
#         {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
#         {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
#         {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."}
#     ])
    
#     model_ = Model()
#     model_.AI_full_retrain_model_pipeline(df=df)

# def test_prediction_pipeline():
#     df = pd.DataFrame([
#         {'label': 0, 'text': "Bonjour, je m'intéresse à vos services"},
#          ])
    
#     model_ = Model(prediction_pipe=True)
#     prediction = model_.AI_full_prediction_pipeline(df=df)
#     assert prediction is not None, prediction