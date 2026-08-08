import sys
import os
import pandas as pd
import logging
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Model import Model
from Business_Rules import Business_Rules
from Mail_Operations import Mail_Operations
from Database import Postgres_DB
from Model import Model
from Set_SpamShield import SET_Spam_Shield_Dependances
from NLP_Feat_Eng import NLP_Feat_Eng
from ML_Flow import ML_Flow_Operations
from Helpers_Monitoring import Helpers_Monitoring
monitor = Helpers_Monitoring()

class SpamShield_Operations():
    def __init__(self):
        pass
    
    @monitor.calculate_func_time
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
        
        
        # stoquer information crypté et version passé au pipeline de préprocessing
        Postgres_DB().save_message(pred_text=pred_text, 
                                raw_text=message['text'].iloc[0], 
                                metadata=metadata,
                                banned_patterns_found=banned_patterns_found,
                                model_pred=bool(prediction_model[0]),
                                model_confidence=model.confidence_score,
                                business_rules_label=bool(prediction_business_rules),
                                final_label=bool(final_label),
                                is_overridden=model.override)
                                   




    @monitor.calculate_func_time
    def Select_Message(self, id):
        selected_message = Postgres_DB().select_message(id)
        return selected_message 
    
    @monitor.calculate_func_time
    def Show_Messages(self, trier_par, filter_par):
        messages = Postgres_DB().get_all_messages(trier_par, filter_par)
        logging.info("Récupération de tous les messages terminée avec succès.")
        return messages

    @monitor.calculate_func_time
    def Dashbord(self):
        data = Postgres_DB().get_dashboard_metrics()
        return data

    @monitor.calculate_func_time
    def Update_label(self, id:int):
        Postgres_DB().update_message_label(id)
        logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")


    @monitor.calculate_func_time
    def Retrain_All_Messages(self):
        #reccupère les messages préprocésé sous forme de liste de dictionnaire
        messages = pd.DataFrame(Postgres_DB().get_all_anonymized_messages())
        model = Model()
        model.AI_full_retrain_model_pipeline(df=messages)
        logging.info("Réentraînement du modèle terminé avec succès.")
        pass

    @monitor.calculate_func_time
    def Delete_All_Messages(self):
        Postgres_DB().delete_all_messages()
        logging.info("Tous les messages ont été supprimés avec succès de la base de données.")

    # DESTINATAIRES
    @monitor.calculate_func_time
    def Get_All_Destinataires(self):
        destinataires = Postgres_DB().get_prospect_mail_front()
        logging.info('Les destinataires ont été réccupérés avec succès')
        return destinataires

    @monitor.calculate_func_time
    def Add_Destinataire(self, prospect:str):
        Postgres_DB().add_prospect_mail([prospect])
        logging.info(f"Le destinataire '{prospect}' a été ajoutée avec succès.")

    @monitor.calculate_func_time
    def Delete_Destinataire(self, id:int):
        Postgres_DB().delete_prospect_mail([id])
        logging.info(f"Le destinataire regex avec l'ID '{id}' a été supprimée avec succès.")    


    # REGEX
    @monitor.calculate_func_time
    def Get_All_Regex_Rules(self):
        regex_rules = Postgres_DB().get_all_regex_rules()
        return regex_rules

    @monitor.calculate_func_time
    def Add_Regex_Rule(self, pattern:str):
        Postgres_DB().add_regex_rule(pattern)
        logging.info(f"La règle regex '{pattern}' a été ajoutée avec succès.")

    @monitor.calculate_func_time
    def Delete_Regex_Rule(self, id:int):
        Postgres_DB().delete_regex_rule(id)
        logging.info(f"La règle regex avec l'ID '{id}' a été supprimée avec succès.")

    # MODEL
    @monitor.calculate_func_time
    def virgin_model(self):
        Model().AI_full_virgin_model_training_pipeline()

    @monitor.calculate_func_time
    def Current_Model_Metrics(self):
        metrics = ML_Flow_Operations().get_latest_model_metrics()
        return metrics
        
    # FORM
    @monitor.calculate_func_time
    def Form_Requirements(self):
        path = f"{os.path.dirname(__file__)}/data/required_metadata.json"
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @monitor.calculate_func_time 
    def Update_Form_Requirements(self, key: str):
        path = f"{os.path.dirname(__file__)}/data/required_metadata.json"

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if key not in data:
            raise KeyError(f"Clé inconnue : {key}")

        data[key] = not data[key]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @monitor.calculate_func_time
    def ML_Test_New_Message(self, message:dict, metadata:dict):
        # Prédiction avec le modèle
        model = Model(prediction_pipe=True, metadata=metadata)
        prediction_model = model.AI_full_prediction_pipeline(message)
        pred_text = model.features['text_final'].iloc[0]
        # Règles métier : regexes, charabia =  forced spam
        business_rules = Business_Rules()
        prediction_business_rules = business_rules.business_rules_ML_test_pipeline(pred_text, metadata)
        if prediction_model[0] or prediction_business_rules:
            final_label = 1
        else:
            final_label = 0

        return final_label

    def check_model_existence(self):
        """Vérifie si un modèle existe dans ML Flow. Si aucun modèle n'existe, il entraîne un modèle vierge."""
        latest_model = ML_Flow_Operations().get_latest_model()
        if latest_model is None:
            logging.info("Aucun modèle existant trouvé dans ML Flow. Entraînement d'un modèle vierge.")
            self.virgin_model()
        else:
            logging.info("Un modèle existant a été trouvé dans ML Flow. Aucun entraînement nécessaire.")
            




    