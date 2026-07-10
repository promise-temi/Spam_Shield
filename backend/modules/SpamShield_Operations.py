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
        model = Model(prediction_pipe=True, metadata=metadata)
        prediction_model = model.AI_full_prediction_pipeline(message)
        pred_text = model.features['text_final'].iloc[0]
        # Règles métier : regexes, charabia =  forced spam
        
        business_rules = Business_Rules()
        prediction_business_rules = business_rules.business_rules_pipeline(pred_text, metadata)
        banned_patterns_found = business_rules.banned_patterns_found
        # si ham envoyer par mail au destinataires, si spam ne rien envoyer(non urgent - nice to hace)
        logging.info(f'model = {prediction_model}, business rules = {prediction_business_rules}')
        # if prediction_model[0] or prediction_business_rules:
        #     logging.info("is spam")
        #     Mail_Operations().send_mail(message['text'].iloc[0], metadata, float(model.confidence_score), "spam")
        #     final_label = 1
        # else:
        #     logging.info(f'Potentielement un message légitime. model = {prediction_model}, business rules = {prediction_business_rules}')
        #     Mail_Operations().send_mail(message['text'].iloc[0], metadata, float(model.confidence_score), "ham")
        #     final_label = 0

        if prediction_model[0] or prediction_business_rules:
            logging.info("is spam")
            Mail_Operations().send_mail(
                message['text'].iloc[0],
                metadata,
                model.confidence_score,
                "spam"
            )

            final_label = 1

        else:
            logging.info(f'Potentiellement un message légitime. model = {prediction_model}, business rules = {prediction_business_rules}')
            Mail_Operations().send_mail(
                message['text'].iloc[0],
                metadata,
                model.confidence_score,
                "ham"
            )
            final_label = 0
        
        if not prediction_model[0]:
            final_label = 0
        # stoquer information crypté et version passé au pipeline de préprocessing
        Postgres_DB().save_message(pred_text=pred_text, 
                                   raw_text=message['text'].iloc[0], 
                                   metadata=metadata,
                                   banned_patterns_found=banned_patterns_found,
                                   model_pred=bool(prediction_model[0]),
                                   model_confidence=model.confidence_score,
                                   business_rules_label=bool(prediction_business_rules),
                                   final_label=bool(final_label))
        
        
    
    def Show_Messages(self):
        Postgres_DB().get_all_messages()
        logging.info("Récupération de tous les messages terminée avec succès.")

    def Update_label(self, id:int):
        Postgres_DB().update_message_label(id)
        logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")

    def Retrain_All_Messages(self):
        #reccupère les messages préprocésé sous forme de liste de dictionnaire
        messages = pd.DataFrame(Postgres_DB().get_all_anonymized_messages())
        model = Model()
        model.AI_full_retrain_model_pipeline(df=messages)
        logging.info("Réentraînement du modèle terminé avec succès.")
        pass

    def Delete_All_Messages(self):
        Postgres_DB().delete_all_messages()
        logging.info("Tous les messages ont été supprimés avec succès de la base de données.")


    def Add_Regex_Rule(self, pattern:str):
        Postgres_DB().add_regex_rule(pattern)
        logging.info(f"La règle regex '{pattern}' a été ajoutée avec succès.")

    def Delete_Regex_rule(self, id:int):
        Postgres_DB().delete_regex_rule(id)
        logging.info(f"La règle regex avec l'ID '{id}' a été supprimée avec succès.")
        


    