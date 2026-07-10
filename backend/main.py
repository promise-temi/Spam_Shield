from modules.Database import Postgres_DB
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import sys
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from modules.SpamShield_Operations import SpamShield_Operations
from modules.Model import Model

Postgres_DB(sql_file_path=f"{os.path.dirname(__file__)}/modules/data/db.sql").create_tables_if_not_exist()
Postgres_DB().add_prospect_mail(['temi.promisejohn@gmail.com'])

# df = pd.DataFrame([{'text':'Je teste mon propre outil de détection de spam, je trouve qu\'il est très efficace !', 'label':1}])
# metadata = {
#     "name":"Promise",
#     "surname":"John",
#     "email":"Promise.john@gmail.com",
#     "phone":"0653389212",
#     "subject":"Je teste mon propre outil de détection de spam :)",
# }

# SpamShield_Operations().New_Message(df, metadata)

# models = [
#     RidgeClassifierModel(),
#     SGDClassifierModel(),
#     RandomForestModel(),
#     CatBoostModel(),
#     LightGBMModel(),
#     FastTextModel(),
#     TransformerModel(),
#     LogisticRegression(),
#     LinearSVC(),
# ]

    

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
# df = pd.DataFrame([{'text':'Je teste mon propre outil de détection de spam, je trouve qu\'il est très efficace ! Si tu est intéressé il y a un site qui fait a peu près la meme chose. je t\'ai mis le lien : https://site_reelement_legitime.xyz', 'label':1}])
# metadata = {
#     "name":"Promise",
#     "surname":"John",
#     "email":"Promise.john@gmail.com",
#     "phone":"0653389212",
#     "subject":"Je teste mon propre outil de détection de spam :)",
# }

# SpamShield_Operations().New_Message(df, metadata)

# metadata = {
#     "name": "test",
#     "surname": "test",
#     "email": "test.test@test.com",
#     "phone": "0653389212",
#     "subject": "SpamShield Test",
# }

# messages = [

#     # HAM
#     "Salut Promise ! On se retrouve demain à 14h pour travailler sur le projet SpamShield ?",
#     "Merci beaucoup pour ton aide hier. Le projet avance vraiment bien grâce à toi.",
#     "Je t’envoie la documentation officielle de Python : https://docs.python.org/3/",
#     "Je viens de publier mon portfolio : https://promise-john.github.io. Dis-moi ce que tu en penses !",
#     "Bonjour, votre commande a été expédiée. Vous recevrez bientôt votre numéro de suivi.",
#     "Bonjour Promise, j’ai découvert ton projet et je souhaiterais échanger avec toi. Voici une démonstration : https://github-demo-security.xyz",
#     "Profitez de -20 % sur tous nos produits ce week-end avec le code ETE20.",
#     "Je teste mon propre outil de détection de spam, je trouve qu'il est très efficace ! Si tu es intéressé il y a un site qui fait à peu près la même chose : https://site_reelement_legitime.xyz",

#     # SPAM
#     "Votre compte bancaire sera suspendu dans 24 heures. Cliquez immédiatement sur https://secure-bank-login.xyz afin de confirmer votre identité.",
#     "Votre colis est bloqué. Payez 2,99€ immédiatement afin d’éviter son retour à l’expéditeur : https://laposte-suivi.xyz",
#     "URGENT : une activité inhabituelle a été détectée sur votre compte. Connectez-vous immédiatement afin d’éviter sa fermeture.",
#     "Support Microsoft : votre ordinateur est infecté. Appelez immédiatement le +33 1 80 00 00 00.",
#     "Félicitations ! Vous avez gagné un iPhone 17 Pro. Cliquez ici pour recevoir votre récompense.",
#     "Votre solde CPF expire aujourd’hui. Activez vos droits avant minuit.",
#     "Le Gouvernement vous informe qu’une amende est en attente. Consultez immédiatement votre dossier.",
#     "Votre assurance maladie nécessite une vérification urgente. Connectez-vous maintenant pour éviter la suspension de vos droits.",
#     "Une tentative de connexion a été détectée depuis la Russie. Vérifiez immédiatement votre compte.",
#     "Bonjour Madame, veuillez confirmer vos informations personnelles immédiatement afin d’éviter le blocage de votre compte.",
#     "Vous avez gagné 1000 euros ! Confirmez votre identité et vos coordonnées bancaires.",
#     "Dernier rappel : votre paiement de 1,99 € est requis pour débloquer votre colis.",
# ]

# for text in messages:
#     df = pd.DataFrame([{"text": text}])
#     SpamShield_Operations().New_Message(df, metadata)


# model = Model(model=LogisticRegression(max_iter=15000, n_jobs=-1, random_state=42), model_name="LogisticRegression")
# model.AI_full_virgin_model_training_pipeline()
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



# model.AI_full_retrain_model_pipeline(df=df)
# df = pd.DataFrame([{'text':'Je teste mon propre outil de détection de spam, je trouve qu\'il est très efficace ! si tu veut esseyez clique sur ce lien : https://faux_site_legitime.com', 'label':1}])
# metadata = {
#     "name":"Promise",
#     "surname":"John",
#     "email":"Promise.john@gmail.com",
#     "phone":"0653389212",
#     "subject":"Je teste mon propre outil de détection de spam :)",
# }


# SpamShield_Operations().New_Message(df, metadata)


# model = Model(model = LogisticRegression(max_iter=1000, n_jobs=-1, random_state=42), model_name="LogisticRegression")
# model.AI_full_virgin_model_training_pipeline()
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

# model.AI_full_retrain_model_pipeline(df=df)




