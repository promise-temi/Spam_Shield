import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Model import Model
from Business_Rules import Business_Rules



class SpamShield_Operations():
    def __init__(self):
        pass

    def New_Message(self, message:dict):
        # Prédiction avec le modèle
        model = Model(prediction_pipe=True)
        prediction_model = model.AI_full_prediction_pipeline(message)

        # Règles métier : regexes, charabia =  forced spam
        regexes = [r"\.net", r"Salut",r"blabla"]
        business_rules = Business_Rules(regexes)
        prediction_business_rules = business_rules.business_rules_pipeline(model.features['text_final'].iloc[0])

        # si ham envoyer par mail au destinataires, si spam ne rien envoyer(non urgent - nice to hace)

        # stoquer information crypté et version passé au pipeline de préprocessing
        pass
    
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


    