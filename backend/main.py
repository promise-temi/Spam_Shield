from modules.Database import Postgres_DB
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import sys
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from modules.SpamShield_Operations import SpamShield_Operations
from modules.Model import Model

Postgres_DB(sql_file_path=f"{os.path.dirname(__file__)}/modules/data/db.sql").create_tables_if_not_exist()

model = Model()
model.AI_full_virgin_model_training_pipeline()
df = pd.DataFrame([
    {'label': 0, 'text': "Bonjour, je m'intéresse à vos services"},
    {'label': 1, 'text': "Gagnez de l'argent rapidement en cliquant ici !"},
    {'label': 0, 'text': "Merci pour votre message. Je vous répondrai bientôt."},
    {'label': 1, 'text': "Offre spéciale : obtenez 50% de réduction sur tous nos produits !"},
    {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
    {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
    {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
    {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
    {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
    {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."},
    {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
    {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
    {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
    {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
    {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
    {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."}
])

model.AI_full_retrain_model_pipeline(df=df)



model = Model(model = LogisticRegression(max_iter=1000, n_jobs=-1, random_state=42), model_name="LogisticRegression")
model.AI_full_virgin_model_training_pipeline()
df = pd.DataFrame([
    {'label': 0, 'text': "Bonjour, je m'intéresse à vos services"},
    {'label': 1, 'text': "Gagnez de l'argent rapidement en cliquant ici !"},
    {'label': 0, 'text': "Merci pour votre message. Je vous répondrai bientôt."},
    {'label': 1, 'text': "Offre spéciale : obtenez 50% de réduction sur tous nos produits !"},
    {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
    {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
    {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
    {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
    {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
    {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."},
    {'label': 0, 'text': "Je suis désolé, mais je ne suis pas intéressé par votre offre."},
    {'label': 1, 'text': "Félicitations ! Vous avez gagné un iPhone. Cliquez ici pour réclamer votre prix."},
    {'label': 0, 'text': "Merci pour votre réponse rapide. Je vais réfléchir à votre proposition."},
    {'label': 1, 'text': "Ne manquez pas cette opportunité unique de gagner de l'argent facilement !"},
    {'label': 0, 'text': "Je vous remercie pour votre temps et votre considération. Bonne journée !"},
    {'label': 1, 'text': "Alerte de sécurité : votre compte a été compromis. Cliquez ici pour sécuriser votre compte."}
])

model.AI_full_retrain_model_pipeline(df=df)




