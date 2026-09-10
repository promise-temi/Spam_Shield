import sys
import os
import pandas as pd
import logging
import datetime
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
from modules.LLModel import LLMModel
from Scheduler import Scheduler
monitor = Helpers_Monitoring()


class SpamShield_Operations():
    def __init__(self):
        pass
    
    
    def New_Message(self, message:dict, metadata:dict):
        try:
            # Prédiction avec le modèle
            monitor.TOTAL_MESSAGE.inc()
            MODEL_INFERENCE_START = time.time()
            model = Model(prediction_pipe=True, metadata=metadata)
            prediction_model = model.AI_full_prediction_pipeline(message)
            pred_text = model.features['text_final'].iloc[0]
            MODEL_INFERENCE_END = time.time()
            MODEL_INFERENCE_TOTAL = (MODEL_INFERENCE_END - MODEL_INFERENCE_START)
            monitor.MODEL_PREDICTION_INFERENCE.set(MODEL_INFERENCE_TOTAL)
            
            # Règles métier : regexes, charabia =  forced spam
            business_rules = Business_Rules()
            prediction_business_rules = business_rules.business_rules_pipeline(pred_text, metadata)
            banned_patterns_found = business_rules.banned_patterns_found

            # si ham envoyer par mail au destinataires, si spam ne rien envoyer(non urgent - nice to hace)
            logging.info(f'model = {prediction_model}, business rules = {prediction_business_rules}')

            if prediction_model[0] or prediction_business_rules:
                logging.info("is spam")
                monitor.TOTAL_SPAM_PREDICTIONS.labels(Model=bool(prediction_model[0]), B_Rules=bool(prediction_model[0])).inc()
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
                monitor.TOTAL_HAM_PREDICTIONS.inc()


            
            # stoquer information crypté et version passé au pipeline de préprocessing
            new_message = Postgres_DB().save_message(pred_text=pred_text, 
                                    raw_text=message['text'].iloc[0], 
                                    metadata=metadata,
                                    banned_patterns_found=banned_patterns_found,
                                    model_pred=bool(prediction_model[0]),
                                    model_confidence=model.confidence_score,
                                    business_rules_label=bool(prediction_business_rules),
                                    final_label=bool(final_label),
                                    is_overridden=model.override)
            
            monitor.CONFIDENCE_SCORE.set(model.confidence_score)
            monitor.MESSAGE_FAILS.set(0)
        except Exception as e:
            logging.error(f"Erreur lors du traitement du message : {e}")
            monitor.MESSAGE_FAILS.set(1)
            raise e



    
    def Select_Message(self, id):
        try:
            selected_message = Postgres_DB().select_message(id)
            return selected_message
        except Exception as e:
            logging.error(f"Erreur lors de la sélection du message : {e}")
    
    def Show_Messages(self, trier_par, filter_par):
        try:
            messages = Postgres_DB().get_all_messages(trier_par, filter_par)
            logging.info("Récupération de tous les messages terminée avec succès.")
            return messages
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des messages : {e}")
            

    def Dashbord(self):
        try:
            data = Postgres_DB().get_dashboard_metrics()
            return data
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des métriques du tableau de bord : {e}")

    def Update_label(self, id:int):
        try:
            Postgres_DB().update_message_label(id)
            logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour du label du message : {e}")
            
    
    def Retrain_All_Messages(self):
        try:
            #reccupère les messages préprocésé sous forme de liste de dictionnaire
            messages = self.get_current_training_data()
            model = Model()
            model.AI_full_retrain_model_pipeline(df=messages)
            self.delete_current_training_data()
            logging.info("Réentraînement du modèle terminé avec succès.")
            monitor.RETRAIN_PIPELINE_FAILS.set(0)
        except Exception as e:
            logging.error(f"Erreur lors du réentraînement du modèle : {e}")
            monitor.RETRAIN_PIPELINE_FAILS.set(1)
    
    def Delete_All_Messages(self):
        try:
            Postgres_DB().delete_all_messages()
            logging.info("Tous les messages ont été supprimés avec succès de la base de données.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de tous les messages : {e}")

    # DESTINATAIRES
    
    def Get_All_Destinataires(self):
        try:
            destinataires = Postgres_DB().get_prospect_mail_front()
            logging.info('Les destinataires ont été réccupérés avec succès')
            return destinataires
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des destinataires : {e}")
        

    
    def Add_Destinataire(self, prospect:str):
        try:
            Postgres_DB().add_prospect_mail([prospect])
            logging.info(f"Le destinataire '{prospect}' a été ajoutée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout du destinataire : {e}")

    
    def Delete_Destinataire(self, id:int):
        try:
            Postgres_DB().delete_prospect_mail([id])
            logging.info(f"Le destinataire regex avec l'ID '{id}' a été supprimée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression du destinataire : {e}")


    # REGEX
    
    def Get_All_Regex_Rules(self):
        try:
            regex_rules = Postgres_DB().get_all_regex_rules()
            logging.info('Les règles regex ont été réccupérés avec succès')
            return regex_rules
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des règles regex : {e}")
        

    
    def Add_Regex_Rule(self, pattern:str):
        try:
            Postgres_DB().add_regex_rule(pattern)
            logging.info(f"La règle regex '{pattern}' a été ajoutée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout de la règle regex : {e}")

    
    def Delete_Regex_Rule(self, id:int):
        try:
            Postgres_DB().delete_regex_rule(id)
            logging.info(f"La règle regex avec l'ID '{id}' a été supprimée avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la règle regex : {e}")

    # MODEL
    
    def virgin_model(self):
        try:
            logging.info("Aucun modèle existant trouvé dans ML Flow. Entraînement d'un modèle vierge.")
            Model().AI_full_virgin_model_training_pipeline()
            monitor.INITIAL_TRAIN_FAILS.set(0)
        except Exception as e:
            logging.error(f"Erreur lors de l'entraînement du modèle vierge : {e}")
            monitor.INITIAL_TRAIN_FAILS.set(1)
            raise
    
    def Current_Model_Metrics(self):
        try:
            metrics = ML_Flow_Operations().get_latest_model_metrics()
            logging.info(metrics)
            try:
                training_data = self.get_current_training_data()
                metrics['training_data'] = training_data.shape[0]
            except Exception as e:
                metrics['training_data'] = 0
            return metrics
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des métriques du modèle actuel : {e}")
        

    def get_current_training_data(self, path=f"{os.path.dirname(__file__)}/data/training_data.parquet"):
        df = pd.read_parquet(path)
        return df

    def delete_current_training_data(self, path=f"{os.path.dirname(__file__)}/data/training_data.parquet"):
        if os.path.exists(path):
            os.remove(path)
            logging.info(f"Données d'entraînement supprimées : {path}")
            return True

        logging.info("Aucune donnée d'entraînement à supprimer.")
        return False

    # FORM
    
    def Form_Requirements(self):
        try:
            path = f"{os.path.dirname(__file__)}/data/required_metadata.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des exigences du formulaire : {e}")

     
    def Update_Form_Requirements(self, key: str, path: str = f"{os.path.dirname(__file__)}/data/required_metadata.json"):
        try:
            path = path

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if key not in data:
                raise KeyError(f"Clé inconnue : {key}")

            data[key] = not data[key]

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour des exigences du formulaire : {e}")

    
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
            return final_label
        except Exception as e:
            logging.error(f"Erreur lors du test du nouveau message : {e}")

    def check_model_existence(self):
        model_path = f"{Model().artifact_path}/model.pkl"
        max_attempts = 5
        delay_seconds = 5
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                logging.info(f"Vérification du modèle - tentative {attempt}/{max_attempts}")
                model_exist = os.path.exists(model_path)
                if not model_exist:
                    logging.info("Aucun modèle existant en local, création du modèle initial.")
                    self.virgin_model()
                else:
                    logging.info("Modèle existant trouvé en local.")
                return
            except Exception as e:
                last_error = e
                logging.warning(f"Échec de la tentative {attempt}/{max_attempts} \n lors de la vérification/initialisation du modèle : {e}")

                if attempt < max_attempts:
                    logging.info(f"Nouvelle tentative dans {delay_seconds} secondes.")
                    time.sleep(delay_seconds)
        monitor.CHECK_MODEL_EXISTANCE_FAILS.set(0)
        # Toutes les tentatives ont échoué
        logging.error(
            f"Impossible de vérifier ou initialiser le modèle "
            f"après {max_attempts} tentatives : {last_error}"
        )
        monitor.CHECK_MODEL_EXISTANCE_FAILS.set(1)
        raise last_error

            

    def llm_report(self):
        try:
            monitor.TOTAL_LLM_CALLS.inc()
            LLM_INFERENCE_START = time.time()
            report_data = LLMModel().generate_report_mistral()
            LLM_INFERENCE_END = time.time()
            LLM_INFERENCE_TOTAL = LLM_INFERENCE_END - LLM_INFERENCE_START
            monitor.TOTAL_LLM_CALLS_FAILS.set(0)
            return report_data
        except Exception as e:
            logging.error(
                f"Erreur lors de la vulgarisation avec le llm - {e}"
            )
            monitor.TOTAL_LLM_CALLS_FAILS.set(1)


    def Set_new_phase(self):
        try:
            phase_end = datetime.datetime.now()
            Scheduler().phase_actions_carence(phase_end=phase_end)
            Scheduler().phase_actions_end(phase_end=phase_end)
            monitor.FLUSH_MESSAGES_FAIL.set(0)
        except Exception as e:
            monitor.FLUSH_MESSAGES_FAIL.set(1)
            raise
