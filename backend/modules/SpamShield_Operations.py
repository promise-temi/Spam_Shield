import sys
import os
import pandas as pd
import logging
import time
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
    
    
    def New_Message(self, message:dict, metadata:dict):
        try:
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

            if prediction_model[0] or prediction_business_rules:
                logging.info("is spam")
                # Mail_Operations().send_mail(
                #     message['text'].iloc[0],
                #     metadata,
                #     model.confidence_score,
                #     "Indésirables"
                # )
                final_label = 1

            else:
                logging.info(f'Potentiellement un message légitime. model = {prediction_model}, business rules = {prediction_business_rules}')
                Mail_Operations().send_mail(
                    message['text'].iloc[0],
                    metadata,
                    model.confidence_score,
                    "Légitimes"
                )
                final_label = 0

            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="New Message", status="success")
        
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
            
            monitor.record_prediction(
                final_label=final_label,
                model_pred=bool(prediction_model[0]),
                business_rules_triggered=bool(prediction_business_rules),
                is_overridden=model.override,
                confidence_score=model.confidence_score,
            )

            monitor.record_banned_patterns(banned_patterns_found)

            monitor.record_gibberish(
                gibberish_score=getattr(business_rules, 'gibberish_score', None)
            )

        except Exception as e:
            logging.error(f"Erreur lors du traitement du message : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="New Message", status="failure", error_type=e)




    
    def Select_Message(self, id):
        try:
            selected_message = Postgres_DB().select_message(id)
            return selected_message
        except Exception as e:
            logging.error(f"Erreur lors de la sélection du message : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Select Message", status="failure", error_type=e)

    def Show_Messages(self, trier_par, filter_par):
        try:
            messages = Postgres_DB().get_all_messages(trier_par, filter_par)
            logging.info("Récupération de tous les messages terminée avec succès.")
            return messages
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des messages : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Show Messages", status="failure", error_type=e)

    
    def Dashbord(self):
        try:
            data = Postgres_DB().get_dashboard_metrics()
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Get Dashboard Metrics", status="success")
            return data
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des métriques du tableau de bord : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Get Dashboard Metrics", status="failure", error_type=e)

    def Update_label(self, id:int):
        try:
            Postgres_DB().update_message_label(id)
            logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")
            monitor.record_label_correction()
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Update Message Label", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du label du message : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Update Message Label", status="failure", error_type=e)

    
    def Retrain_All_Messages(self):
        try:
            #reccupère les messages préprocésé sous forme de liste de dictionnaire
            messages = pd.DataFrame(Postgres_DB().get_all_anonymized_messages())
            model = Model()
            model.AI_full_retrain_model_pipeline(df=messages)
            logging.info("Réentraînement du modèle terminé avec succès.")
            monitor.record_model_retrain(is_success=True)
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Retrain Model", status="success")
        except Exception as e:
            logging.error(f"Erreur lors du réentraînement du modèle : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Retrain Model", status="failure", error_type=e)
        

    
    def Delete_All_Messages(self):
        try:
            Postgres_DB().delete_all_messages()
            logging.info("Tous les messages ont été supprimés avec succès de la base de données.")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Delete All Messages", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de tous les messages : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Delete All Messages", status="failure", error_type=e)

    # DESTINATAIRES
    
    def Get_All_Destinataires(self):
        try:
            destinataires = Postgres_DB().get_prospect_mail_front()
            logging.info('Les destinataires ont été réccupérés avec succès')
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Get All Destinataires", status="success")
            return destinataires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des destinataires : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Get All Destinataires", status="failure", error_type=e)
        

    
    def Add_Destinataire(self, prospect:str):
        try:
            Postgres_DB().add_prospect_mail([prospect])
            logging.info(f"Le destinataire '{prospect}' a été ajoutée avec succès.")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Add Destinataire", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du destinataire : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Add Destinataire", status="failure", error_type=e)

    
    def Delete_Destinataire(self, id:int):
        try:
            Postgres_DB().delete_prospect_mail([id])
            logging.info(f"Le destinataire regex avec l'ID '{id}' a été supprimée avec succès.")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Delete Destinataire", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du destinataire : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Delete Destinataire", status="failure", error_type=e)


    # REGEX
    
    def Get_All_Regex_Rules(self):
        try:
            regex_rules = Postgres_DB().get_all_regex_rules()
            logging.info('Les règles regex ont été réccupérés avec succès')
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Get All Regex Rules", status="success")
            return regex_rules
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des règles regex : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Get All Regex Rules", status="failure", error_type=e)
        

    
    def Add_Regex_Rule(self, pattern:str):
        try:
            Postgres_DB().add_regex_rule(pattern)
            logging.info(f"La règle regex '{pattern}' a été ajoutée avec succès.")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Add Regex Rule", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout de la règle regex : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Add Regex Rule", status="failure", error_type=e)

    
    def Delete_Regex_Rule(self, id:int):
        try:
            Postgres_DB().delete_regex_rule(id)
            logging.info(f"La règle regex avec l'ID '{id}' a été supprimée avec succès.")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Delete Regex Rule", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la règle regex : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Delete Regex Rule", status="failure", error_type=e)

    # MODEL
    
    def virgin_model(self):
        try:
            logging.info("Aucun modèle existant trouvé dans ML Flow. Entraînement d'un modèle vierge.")
            Model().AI_full_virgin_model_training_pipeline()
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Virgin Model Training", status="success")
        except Exception as e:
            logging.error(f"Erreur lors de l'entraînement du modèle vierge : {e}")
            monitor.record_virgin_model_training(is_success=True)
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Virgin Model Training", status="failure", error_type=e)

    
    def Current_Model_Metrics(self):
        try:
            metrics = ML_Flow_Operations().get_latest_model_metrics()
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Get Current Model Metrics", status="success")
            return metrics
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des métriques du modèle actuel : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Get Current Model Metrics", status="failure", error_type=e)
        
        
    # FORM
    
    def Form_Requirements(self):
        try:
            path = f"{os.path.dirname(__file__)}/data/required_metadata.json"
            with open(path, "r", encoding="utf-8") as f:
                monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Get Form Requirements", status="success")
                return json.load(f)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des exigences du formulaire : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Get Form Requirements", status="failure", error_type=e)

     
    def Update_Form_Requirements(self, key: str, path: str = f"{os.path.dirname(__file__)}/data/required_metadata.json"):
        try:
            path = path

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if key not in data:
                raise KeyError(f"Clé inconnue : {key}")

            data[key] = not data[key]

            with open(path, "w", encoding="utf-8") as f:
                monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="Update Form Requirements", status="success")
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour des exigences du formulaire : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="Update Form Requirements", status="failure", error_type=e)

    
    def ML_Test_New_Message(self, message:dict, metadata:dict):
        try:
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
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=True, name="ML Test New Message", status="success")
            return final_label
        except Exception as e:
            logging.error(f"Erreur lors du test du nouveau message : {e}")
            monitor.record_methode_result(pipe_type="Spamshield Operations", is_success=False, name="ML Test New Message", status="failure", error_type=e)


    def check_model_existence(self):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                latest_model = ML_Flow_Operations().get_latest_model()
                if latest_model is None:
                    logging.info("Aucun modèle trouvé, entraînement d'un modèle vierge.")
                    self.virgin_model()
                else:
                    logging.info("Modèle existant trouvé dans MLflow.")
                monitor.record_methode_result(
                    pipe_type="Spamshield Operations",
                    is_success=True,
                    name="Check Model Existence",
                    status="success"
                )
                monitor.record_model_existence_check(is_success=True)
                return  # succès → on sort
            except Exception as e:
                logging.warning(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)  # attend 5 secondes avant de réessayer
                else:
                    logging.error("MLflow inaccessible après plusieurs tentatives.")
                    monitor.record_methode_result(
                        pipe_type="Spamshield Operations",
                        is_success=False,
                        name="Check Model Existence",
                        status="failure",
                        error_type=e
                    )



    