import re
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Markov_Model import MarkovGibberishDetector


class Business_Rules:
    def __init__(self, patterns:list[str], min_lenght_message:int=5, max_lenght_message:int=50_000):
        self.banned_patterns_found = []
        self.patterns = patterns
        self.min_size_message = min_lenght_message
        self.max_size_message = max_lenght_message
        self.detector = MarkovGibberishDetector()


    def business_rules_pipeline(self, text:str)->int :
        self.filter_message_lenght(text)
        self.gibberish(text)
        self.banned_patterns(text)
        is_spam = self.delibaration(text)
        return is_spam
        


    def gibberish(self, text:str):
        self.detector.train_model(pd.read_parquet(f"{os.path.dirname(__file__)}/data/corpus.parquet"))
        is_giberish = self.detector.is_gibberish(text)
        if is_giberish:
            self.banned_patterns_found.append(f"Contient charabia/gibberish  : {len(text)}.")

    def filter_message_lenght(self, text:str):
        if len(text) < self.min_size_message:
            self.banned_patterns_found.append(f"Message trop court : {len(text)}.")
        if len(text) > self.max_size_message:
            self.banned_patterns_found.append(f"Message trop long : {len(text)}.")


    def banned_patterns(self, text:str):
        for pattern in self.patterns:
            banned_pattern = re.match(fr"{pattern}", text)
            if banned_pattern:
                self.banned_patterns_found.append(f"Contient pattern interdit : {pattern}.")


    def delibaration(self)->int:
        if self.banned_patterns_found:
            return 1 #spam
        else:
            return 0 #ham

    

    
