import sys
import os
import pandas as pd
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Model import Model
from Business_Rules import Business_Rules
from Mail_Operations import Mail_Operations
from Database import Postgres_DB



class SpamShield_Operations():
    def __init__(self):
        pass

    def New_Message(self, message:dict, metadata:dict):
        # Prédiction avec le modèle
        model = Model(prediction_pipe=True)
        prediction_model = model.AI_full_prediction_pipeline(message)
        pred_text = model.features['text_final'].iloc[0]
        # Règles métier : regexes, charabia =  forced spam
        
        business_rules = Business_Rules()
        prediction_business_rules = business_rules.business_rules_pipeline(pred_text, metadata)
        banned_patterns_found = business_rules.banned_patterns_found
        # si ham envoyer par mail au destinataires, si spam ne rien envoyer(non urgent - nice to hace)
        logging.info(f'model = {prediction_model}, business rules = {prediction_business_rules}')
        if prediction_model[0] or prediction_business_rules:
            logging.info("is spam")
            final_label = 1
        else:
            logging.info(f'Potentielement un message légitime. model = {prediction_model}, business rules = {prediction_business_rules}')
            Mail_Operations().send_mail(message['text'].iloc[0], metadata)
            final_label = 0
        # stoquer information crypté et version passé au pipeline de préprocessing
        Postgres_DB().save_message(pred_text=pred_text, 
                                   raw_text=message['text'].iloc[0], 
                                   metadata=metadata, 
                                   banned_patterns_found=banned_patterns_found, 
                                   model_pred=bool(prediction_model[0]), 
                                   business_rules_label=bool(prediction_business_rules), 
                                   final_label=bool(final_label))
        
        
    
    def Show_Messages(self):
        #reccuperer tout les messages
        # decrypter informations
        # preparer liste de dictionnaires de messages
        pass

    def Update_label(self, id:int):
        # prendre en entrée l'id 
        # mettre a jour le label (passer la var modified a l'opposé)
        pass

    def Retrain_All_Messages(self):
        #reccupère les messages préprocésé sous forme de liste de dictionnaire
        # réentraine le model
        pass

    def Delete_All_Messages(self):
        #supprime tout les messages de la base de données 
        pass

    def Send_Report(self):
        # Envoi le rapport
        pass

    def Add_Regex_Rule(self):
        # A jout dans la base les nouvelles regex
        pass

    def Delete_Regex_rule(self):
        # Suppression dans la base regex
        pass


    