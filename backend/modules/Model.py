import pandas as pd
import re
import numpy as np
import nltk
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
import regex



class Model:
    def __init__(self, path_original_data):
        self.original_df = pd.read_parquet(path_original_data)
        self.df = self.original_df.copy()

    def __set_nltk_french_stop_words(self):
        """Cette méthode télécharge les stop words depuis nltk, 
        en français et les stocke dans un attribut de la classe.
        """
        nltk.download('stopwords')
        stemmer = FrenchStemmer()
        stop_words = set(stopwords.words("french"))
        self.stop_words = stop_words

    def remove_stopwords(self, text):
        words = text.split()

        filtered_words = []

        for word in words:
            
            # garder les tokens
            if word.startswith("[") and word.endswith("]"):
                filtered_words.append(word)

            # retirer stopwords normaux
            elif word.lower() not in self.stop_words:
                filtered_words.append(word)

        return " ".join(filtered_words)
    
    def clean_stopwords(self, text):
        """Cette méthode nettoie les stop words d'un texte donné.
        Elle utilise la méthode remove_stopwords pour retirer les stop words
        et retourne le texte nettoyé.
        """
        self.df["text_final"] = self.df['text_final'].apply(self.remove_stopwords)
