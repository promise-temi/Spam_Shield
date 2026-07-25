import re
import pandas as pd
import os
import sys
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Markov_Model import MarkovGibberishDetector
from NLP_Feat_Eng import NLP_Feat_Eng
from Database import Postgres_DB
import json

class Business_Rules:
    def __init__(self, min_lenght_message:int=5, max_lenght_message:int=50_000):
        self.banned_patterns_found = []
        self.min_size_message = min_lenght_message
        self.max_size_message = max_lenght_message
        db = Postgres_DB()
        self.patterns = db.get_regexes_patterns() 
        
        with open(f"{os.path.dirname(__file__)}/data/required_metadata.json", "r", encoding="utf-8") as f:
            self.metadata_values = json.load(f)
        self.name_presence = self.metadata_values['name']
        self.surname_presence = self.metadata_values['surname']
        self.email_presence = self.metadata_values['email']
        self.phone_presence = self.metadata_values['phone']
        self.subject_presence = self.metadata_values['subject']
        self.gibberish_presence = self.metadata_values['gibberish']
        self.detector = MarkovGibberishDetector()
        


    def business_rules_pipeline(self, text:str, metadata)->int :
        self.filter_message_lenght(text)
        if self.gibberish_presence:
            self.gibberish(text)
        self.banned_patterns(text)
        self.metadata_rules_pipeline(metadata)
        is_spam = self.delibaration()
        print(self.banned_patterns_found)
        return is_spam
        
    
    def business_rules_ML_test_pipeline(self, text:str, metadata)->int :
        self.filter_message_lenght(text)
        if self.gibberish_presence:
            self.gibberish(text)
        is_spam = self.delibaration()
        print(self.banned_patterns_found)
        return is_spam

    def gibberish(self, text:str):
        df = pd.read_parquet(f"{os.path.dirname(__file__)}/data/corpus.parquet")
        self.detector.train_model(df["token"].tolist())
        is_giberish = self.detector.is_gibberish(text)
        print(f"giberish score = {self.detector.score_}")
        if is_giberish:
            self.banned_patterns_found.append(f"Contient charabia/gibberish : {self.detector.score_}.")

    def filter_message_lenght(self, text:str):
        if len(text) < self.min_size_message:
            self.banned_patterns_found.append(f"Message trop court : {len(text)}.")
        if len(text) > self.max_size_message:
            self.banned_patterns_found.append(f"Message trop long : {len(text)}.")


    def banned_patterns(self, text:str):
        if len(self.patterns) >= 1:
            for pattern in self.patterns:
                banned_pattern = re.match(fr"{pattern}", text)
                if banned_pattern:
                    self.banned_patterns_found.append(f"Contient pattern interdit : {pattern}.")




    def delibaration(self)->int:
        if self.banned_patterns_found:
            return 1 #spam
        else:
            return 0 #ham

    def metadata_rules_pipeline(self, metadata:object):
        logging.info(f"Metadata_Business_Rules initialized with name_presence={self.name_presence}, surname_presence={self.surname_presence}, email_presence={self.email_presence}, phone_presence={self.phone_presence}, subject_presence={self.subject_presence}, gibberish_presence={self.gibberish_presence}")

        print(metadata)
        self.check_name(metadata['name'])
        self.check_surname(metadata['surname'])
        self.check_email(metadata['email'])
        self.check_phone(metadata['phone'])
        self.check_subject(metadata['subject'])

    def feat_eng_metadata(self, text):
        df = pd.DataFrame([{"text":text}])
        tools_ = NLP_Feat_Eng(df)
        tools_.message_length()
        tools_.special_character_count()
        tools_.special_character_ratio()
        tools_.digit_count()
        tools_.phone_number_count()
        tools_.email_count()
        tools_.company_email_count()
        tools_.support_email_count()
        tools_.suspect_email_count()
        tools_.email_count()
        tools_.support_email_count()
        tools_.lower_the_text()
        tools_.count_urls()
        tools_.count_shortened_urls()
        tools_.count_suspicious_urls()
        return tools_.df
    
    def check_name(self, name):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.name_presence == True:
            if name == "" or name == False or name == None:
                self.banned_patterns_found.append(f"le Prenomom est obligatoire mais n'a pas été renseigné.")
                return
        elif self.name_presence == False:
            return

            
        self.gibberish(name)

        df = self.feat_eng_metadata(name).iloc[0]
        
        if df['msg_length'] <= 2 or df['msg_length'] >= 50:
            self.banned_patterns_found.append(f"le Prenom semble anormalement court ou anormalement long.")

            
        if df['digit_count'] > 2:
            self.banned_patterns_found.append(f"Le Prenom contient des chiffre, ce qui est inhabituel.")
            
        
        if df['email_count'] > 0:
            self.banned_patterns_found.append(f"Une addresse email à été détectée dans le champs Prenom")
            
        
        if df['phone_number_count'] > 0:
            self.banned_patterns_found.append(f"Un numero de téléphone à été détectée dans le champs Prenom")
            
        
        if df['url_count'] > 0:
            self.banned_patterns_found.append(f"Une URL à été détectée dans le champs Prenom")
        
        
        if df['special_character_ratio'] > 0.25:
            self.banned_patterns_found.append(f"Le Prenom contient un nombre inhabituel de characères spéciaux")
            
        
        


    def check_surname(self, surname):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.surname_presence == True:
            if surname == "" or surname == False or surname == None:
                self.banned_patterns_found.append(f"le Nom est obligatoire mais n'a pas été renseigné.")
                return
        if self.surname_presence == False:
            return
            
        self.gibberish(surname)
        df = self.feat_eng_metadata(surname).iloc[0]
        
        if df['msg_length'] <= 2 or df['msg_length'] >= 80:
            self.banned_patterns_found.append(f"le Nom semble anormalement court ou anormalement long.")
            
        if df['digit_count'] > 3:
            self.banned_patterns_found.append(f"Le Nom contient des chiffre, ce qui est inhabituel.")
            
        
        if df['email_count'] > 0:
            self.banned_patterns_found.append(f"Une addresse email à été détectée dans le champs Nom")
            
        
        if df['phone_number_count'] > 0:
            self.banned_patterns_found.append(f"Un numero de téléphone à été détectée dans le champs Nom")
            
        
        if df['url_count'] > 0:
            self.banned_patterns_found.append(f"Une URL à été détectée dans le champs Nom")
        
        
        if df['special_character_ratio'] > 0.25:
            self.banned_patterns_found.append(f"Le nom contient un nombre inhabituel de characères spéciaux")
            
        



    def check_email(self, email):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.email_presence == True:
            if email == "" or email == False or email == None:
                self.banned_patterns_found.append(f"L'email est obligatoire mais n'a pas été renseigné.")
                return
        elif self.email_presence == False:
            return
            
        df = self.feat_eng_metadata(email).iloc[0]

        if df['email_count'] == 0:
            self.banned_patterns_found.append(f"Aucune addresse email n'à été détectée dans le champs Email")
            
            
        if df['suspect_email_count'] > 0:
            self.banned_patterns_found.append(f"Une addresse email suspecte à été détectée dans le champs Email")
            
        
        if df['msg_length'] <= 6 or df['msg_length'] >= 254:
            self.banned_patterns_found.append(f"L'email' semble anormalement courte ou anormalement longue.")
            

    def check_phone(self, phone):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.phone_presence == True:
            if phone == "" or phone == False or phone == None:
                self.banned_patterns_found.append(f"Le telephone est obligatoire mais n'a pas été renseigné.")
                return
        elif self.phone_presence == False:
            return
            
        df = self.feat_eng_metadata(phone).iloc[0]

        if df['phone_number_count'] < 1:
            self.banned_patterns_found.append(f"Aucun numero de téléphone détecté dans le champs Telephone.")
            
    
    def check_subject(self, subject):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.subject_presence == True:
            if subject == "" or subject == False or subject == None:
                self.banned_patterns_found.append(f"L'objet est obligatoire mais n'a pas été renseigné.")
                return
        elif self.subject_presence == False:
            return
            
        df = self.feat_eng_metadata(subject).iloc[0]

        if df['msg_length'] <= 2 or df['msg_length'] >= 180:
            self.banned_patterns_found.append(f"l'objet' semble anormalement court ou anormalement long.")

        if df['suspect_email_count'] > 0:
            self.banned_patterns_found.append(f"Une addresse email suspecte à été détectée dans le champs Objet")

        if df['suspicious_url_count'] > 0 or df['shortened_url_count'] > 0:
            self.banned_patterns_found.append(f"Une url suspecte à été détectée dans le champs Objet")
          
            
    
        

    
    
    
    
