import pandas as pd
import re
import numpy as np
import nltk
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from scipy.sparse import hstack



class Preprocessing:
    def __init__(self, df):
        self.df = df
        self.__set_nltk_french_stop_words()
        self.text_col = "text_final"
        self.target_col = "label"
        self.exclude_cols = ["text", "label", "text_transformed", "text_final", "text_preprocessed"]

    def __set_nltk_french_stop_words(self):
        """Cette méthode télécharge les stop words depuis nltk, 
        en français et les stocke dans un attribut de la classe.
        """
        nltk.download('stopwords')
        self.stemmer = FrenchStemmer()
        self.stop_words = set(stopwords.words("french"))
        

    def preprossessing_pipeline(self):
        """Cette méthode exécute l'ensemble du pipeline de prétraitement sur le DataFrame.
        Elle applique les différentes étapes de nettoyage et de transformation des données
        pour préparer les textes à l'analyse ultérieure.
        """
        self.df["text_preprocessed"] = self.df[self.text_col].apply(self.clean_text)
        self.clean_stopwords()
        self.apply_stemming()
        self.normalize_and_space_tokens()
        self.relace_inf_with_zero()
        self.drop_duplicates_()
        self.train_test_split()
        self.tfidf_vectorization()
        self.robust_scale_numeric_features()
        self.hsstack_features()
        return self.X_train_combined, self.X_test_combined, self.y_train, self.y_test


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
    
    def clean_stopwords(self):
        """Cette méthode nettoie les stop words d'un texte donné.
        Elle utilise la méthode remove_stopwords pour retirer les stop words
        et retourne le texte nettoyé.
        """
        self.df["text_preprocessed"] = self.df["text_preprocessed"].apply(self.remove_stopwords)

    def stem_text(self, text):
        words = text.split()

        stemmed_words = []

        for word in words:

            # protéger tokens
            if word.startswith("[") and word.endswith("]"):
                stemmed_words.append(word)

            else:
                stemmed_words.append(self.stemmer.stem(word))

        return " ".join(stemmed_words)
    
    
    def apply_stemming(self):
        """Cette méthode applique la racinisation (stemming) à un texte donné.
        Elle utilise la méthode stem_text pour transformer les mots en leurs racines
        et retourne le texte transformé.
        """
        self.df["text_preprocessed"] = self.df["text_preprocessed"].apply(self.stem_text)

    def normalize_tokens(self, text):
        return re.sub(r"\[([a-zA-Z]+)\]", lambda m: "[" + m.group(1).upper() + "]", text)

    def space_tokens(self, text):
        text = re.sub(r"(\[[A-Z]+\])", r" \1 ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    
    def normalize_and_space_tokens(self):
        """Cette méthode normalise et espace les tokens d'un texte donné.
        Elle utilise les méthodes normalize_tokens et space_tokens pour transformer
        les tokens en majuscules et les espacer correctement, puis retourne le texte transformé.
        """
        self.df['text_preprocessed'] = self.df['text_preprocessed'].apply(self.normalize_tokens)
        self.df['text_preprocessed'] = self.df['text_preprocessed'].apply(self.space_tokens)
        
    def relace_inf_with_zero(self):
        """Cette méthode remplace les valeurs infinies et NaN dans le DataFrame par des zéros.
        Elle utilise la méthode replace de pandas pour effectuer cette transformation
        et retourne le DataFrame modifié.
        """
        self.df = self.df.replace([np.inf, -np.inf], np.nan).fillna(0)

    def drop_duplicates_(self):
        """Cette méthode supprime les doublons du DataFrame.
        Elle utilise la méthode drop_duplicates de pandas pour éliminer les lignes en double
        et retourne le DataFrame modifié.
        """
        self.df = self.df.drop_duplicates(subset=["text_preprocessed"], keep="first").reset_index(drop=True)

    def train_test_split(self,  test_size=0.2, random_state=42):
        """Cette méthode divise le DataFrame en ensembles d'entraînement et de test.
        Elle utilise la fonction train_test_split de scikit-learn pour effectuer cette division
        en fonction de la taille du test et de l'état aléatoire spécifiés, puis retourne les ensembles d'entraînement et de test.
        """
        feature_cols = [col for col in self.df.columns if col not in self.exclude_cols]
        self.X_text = self.df["text_preprocessed"]
        self.X_num = self.df[feature_cols]
        self.y = self.df['label']

        self.X_text_train, self.X_text_test, self.X_num_train, self.X_num_test, self.y_train, self.y_test = train_test_split(
            self.X_text,
            self.X_num,
            self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y
        )

    def tfidf_vectorization(self):
        """Cette méthode applique la vectorisation TF-IDF aux textes d'entraînement et de test.
        Elle utilise la classe TfidfVectorizer de scikit-learn pour transformer les textes en matrices de caractéristiques
        basées sur la fréquence des termes, puis retourne les matrices d'entraînement et de test.
        """
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )

        self.X_text_train_tfidf = vectorizer.fit_transform(self.X_text_train)
        self.X_text_test_tfidf = vectorizer.transform(self.X_text_test)

    
    def robust_scale_numeric_features(self):
        """Cette méthode applique la normalisation robuste aux caractéristiques numériques d'entraînement et de test.
        Elle utilise la classe RobustScaler de scikit-learn pour transformer les caractéristiques numériques
        en utilisant la médiane et l'écart interquartile, puis retourne les matrices d'entraînement et de test normalisées.
        """
        scaler = RobustScaler()
        self.X_num_train_scaled = scaler.fit_transform(self.X_num_train)
        self.X_num_test_scaled = scaler.transform(self.X_num_test)

    def hsstack_features(self):
        """Cette méthode combine les caractéristiques textuelles vectorisées et les caractéristiques numériques normalisées.
        Elle utilise la fonction hstack de scipy pour empiler horizontalement les matrices de caractéristiques
        et retourne les matrices d'entraînement et de test combinées.
        """
        self.X_test_combined = hstack([self.X_text_test_tfidf, self.X_num_test_scaled])
        self.X_train_combined = hstack([self.X_text_train_tfidf, self.X_num_train_scaled])