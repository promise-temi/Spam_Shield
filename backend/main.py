import pandas as pd
from modules.Model import Model
from modules.Set_SpamShield import SET_Spam_Shield_Dependances
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# build virgin model pipeline

df_messages = SET_Spam_Shield_Dependances(raw_data_dir="backend/modules/data/raw_data").Dependances_Full_Pipeline(lang='fr')
print(type(df_messages))

model_ = Model()
model_.AI_full_virgin_model_training_pipeline(df_messages, "backend/modules/data/corpus.parquet")

# model_ = Model()
# model_.AI_full_virgin_model_training_pipeline(df=pd.read_parquet("data/spam_ham_dataset.parquet"))

# # retrain model pipeline
# model_ = Model()
# df = pd.DataFrame([
#     {'label': 0, 'text': "Bonjour, je m'intéresse à vos services"},
#     {'label': 1, 'text': "Gagnez de l'argent rapidement en cliquant ici !"},
#     {'label': 0, 'text': "Merci pour votre message. Je vous répondrai bientôt."},
#     {'label': 1, 'text': "Offre spéciale : obtenez 50% de réduction sur tous nos produits !"},
#     {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
#     {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
#     {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
#     {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
#     {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
#     {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."},
#     {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
#     {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
#     {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
#     {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
#     {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
#     {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."}
# ])
# model_.AI_full_retrain_model_pipeline(df=df)


# # prediction pipeline
# df = pd.DataFrame([
#         {'label': None, 'text': "bim bam booum !"},
#          ])
    
# model_ = Model(prediction_pipe=True)
# prediction = model_.AI_full_prediction_pipeline(df=df)
# print(df["text"].iloc[0])
# print(prediction)