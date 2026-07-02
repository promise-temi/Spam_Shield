import re
import pandas as pd
import os
import sys
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Markov_Model import MarkovGibberishDetector
from Database import Postgres_DB


class Metadata_Business_Rules:
    def __init__(self):
        db = Postgres_DB()
        self.name_presence = db.select_metadata_value('name')
        self.surname_presence = db.select_metadata_value('surname')
        self.email_presence = db.select_metadata_value('email')
        self.phone_presence = db.select_metadata_value('phone')
        self.subject_presence = db.select_metadata_value('subject')
        self.gibberish_presence = db.select_metadata_value('gibberish')
        self.detector = MarkovGibberishDetector()
        

    def gibberish(self, text:str):
        df = pd.read_parquet(f"{os.path.dirname(__file__)}/data/corpus.parquet")
        self.detector.train_model(df["token"].tolist())
        is_giberish = self.detector.is_gibberish(text)
        print(f"giberish score = {self.detector.score_}")
        if is_giberish:
            return False

    def metadata_rules_pipeline(self, metadata:object):
        self.check_name(metadata['name'])
        self.check_surname(metadata['surname'])
        self.check_email(metadata['email'])
        self.check_phone(metadata['phone'])
        self.check_subject(metadata['subject'])

    
    
    def check_name(self, name, tool_df):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.name_presence:
            if name == "" or name == False or name == None:
                return False
            
        self.gibberish(name)

        df = tool_df.iloc[0]
        
        if df['msg_length'] <= 2 or df['msg_length'] >= 50:
            return False
            
        if df['digit_count'] > 2:
            return False
            
        
        if df['email_count'] > 0:
            return False
        
        if df['phone_number_count'] > 0:
            return False
        
        if df['url_count'] > 0:
            return False
        
        if df['special_character_ratio'] > 0.25:
            return False
        
        return True
        


    def check_surname(self, surname, tool_df):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.surname_presence:
            if surname == "" or surname == False or surname == None:
                return False
            
        self.gibberish(surname)
        df = tool_df.iloc[0]
        
        if df['msg_length'] <= 2 or df['msg_length'] >= 80:
            return False
            
        if df['digit_count'] > 3:
            return False
            
        
        if df['email_count'] > 0:
            return False
            
        
        if df['phone_number_count'] > 0:
            return False
            
        
        if df['url_count'] > 0:
            return False
        
        
        if df['special_character_ratio'] > 0.25:
            return False
        
        return True
        



    def check_email(self, email, tool_df):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.email_presence:
            if email == "" or email == False or email == None:
                return False
            
        df = tool_df.iloc[0]

        if df['email_count'] == 0:
            return False
            
            
        if df['suspect_email_count'] > 0:
            return False
            
        
        if df['msg_length'] <= 6 or df['msg_length'] >= 254:
            return False
        
        return True
            

    def check_phone(self, phone, tool_df):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.phone_presence:
            if phone == "" or phone == False or phone == None:
                return False
            
        df = tool_df.iloc[0]

        if df['phone_number_count'] < 1:
            return False
        
        return True
            
    
    def check_subject(self, subject, tool_df):
        # l'utilisateur peut vouloir que l'on verifie ce champs ou non, mais si il ny a pas de donnée qu'il ecrive no name par défaut
        if self.subject_presence:
            if subject == "" or subject == False or subject == None:
                return False
            
        df = tool_df.iloc[0]

        if df['msg_length'] <= 2 or df['msg_length'] >= 180:
            return False

        if df['suspect_email_count'] > 0:
            return False

        if df['suspicious_url_count'] > 0 or df['shortened_url_count'] > 0:
            return False
        
        return True
          
            
    
        

    
    
    
    
