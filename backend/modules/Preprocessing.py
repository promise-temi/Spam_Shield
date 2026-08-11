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
from sklearn.decomposition import PCA
from scipy.sparse import hstack
import joblib
import sys
import os
import logging
from sklearn.decomposition import TruncatedSVD
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from ML_Flow import ML_Flow_Operations
from Helpers_Monitoring import Helpers_Monitoring
monitor = Helpers_Monitoring()

class Preprocessing:
    def __init__(self, df, artifact_path="", prediction_pipe=False):
        self.df = df
        self.__set_nltk_french_stop_words()
        self.text_col = "text_final"
        self.target_col = "label"
        self.exclude_cols = ["text", "label", "text_transformed", "text_final", "text_preprocessed", 'text_lower', 'lang', 'sample_weight']
        self.prediction_pipe = prediction_pipe
        self.artifact_path = artifact_path

    def __set_nltk_french_stop_words(self):
        """Cette méthode télécharge les stop words depuis nltk, 
        en français et les stocke dans un attribut de la classe.
        """
        nltk.download('stopwords')
        self.stemmer = FrenchStemmer()
        self.stop_words = set(stopwords.words("french"))
        
    
    @monitor.calculate_func_time
    def preprocessing_pipeline(self):
        """Cette méthode exécute l'ensemble du pipeline de prétraitement sur le DataFrame.
        Elle applique les différentes étapes de nettoyage et de transformation des données
        pour préparer les textes à l'analyse ultérieure.
        """
        logging.info("Début du pipeline de preprocessing NLP")
        self.df["text_preprocessed"] = self.df[self.text_col]
        self.clean_stopwords()
        self.apply_stemming()
        self.normalize_and_space_tokens()
        self.relace_inf_with_zero()
        self.drop_duplicates_()
        self.memory_data()
        if self.prediction_pipe:
            self.split_for_prediction()
        else:
            self.train_test_split()
        self.tfidf_vectorization(self.artifact_path)
        self.robust_scale_numeric_features(self.artifact_path)
        self.dimension_reduction_truncated_SVD(self.artifact_path)
        self.dimension_reduction_pca(self.artifact_path)
        self.np_hsstack_features()
        logging.info("Fin du pipeline de preprocessing NLP")
        if self.prediction_pipe:
            return self.X_train_combined
        
        return self.X_train_combined, self.X_test_combined, self.y_train, self.y_test, self.sample_weight_train, self.sample_weight_test

    
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

    
    def delete_memory_data(self):
        memory_path = f"{self.artifact_path}/memory_df.parquet"

        if os.path.exists(memory_path):
            os.remove(memory_path)
            logging.info("Fichier mémoire supprimé avec succès.")
        else:
            logging.info("Aucun fichier mémoire à supprimer.")

    
    def memory_data(self):
        
        if self.prediction_pipe:
            self.df_memory = self.df.copy()
            return
        
        memory_path = f"{self.artifact_path}/memory_df.parquet"
        os.makedirs(self.artifact_path, exist_ok=True)

        if "text_preprocessed" not in self.df.columns:
            raise ValueError("La colonne text_preprocessed doit exister avant __memory_data().")
        # récupération et nettoyage du nouveau df
        df_new = self.df.copy()
        df_new = df_new.drop_duplicates(subset=["text_preprocessed"], keep="last")
        # si parquet existant
        if os.path.exists(memory_path):
            # recupération de l'ancien df
            df_memory = pd.read_parquet(memory_path)
            self.df_memory = df_memory.copy()
            # concaténation 
            df_memory_all = pd.concat([df_memory, df_new], ignore_index=True)
            df_memory_all = df_memory_all.drop_duplicates(subset=["text_preprocessed"], keep="last")
            self.retrain_pipe = True
        else:
            # si il n'existe pas reccupation simple du nouveau df
            df_memory_all = df_new
            self.df_memory = df_new
            self.retrain_pipe = False
            
        # enregistrement du nouveau df
        df_memory_all.to_parquet(memory_path, index=False)
        



    
    def split_for_prediction(self):
        feature_cols = [col for col in self.df.columns if col not in self.exclude_cols]

        print(feature_cols)

        self.X_text = self.df["text_preprocessed"]
        self.X_num = self.df[feature_cols]

        if self.prediction_pipe:
            self.X_text_train = self.X_text
            self.X_num_train = self.X_num
            

    
    def train_test_split(self, test_size=0.2, random_state=42):
        """Cette méthode divise le DataFrame en ensembles d'entraînement et de test.
        Elle utilise la fonction train_test_split de scikit-learn pour effectuer cette division
        en fonction de la taille du test et de l'état aléatoire spécifiés, puis retourne les ensembles d'entraînement et de test.
        """
        self.df_memory["sample_weight"] = 1.0
        feature_cols = [col for col in self.df_memory.columns if col not in self.exclude_cols]

        self.X_text = self.df_memory["text_preprocessed"]
        self.X_num = self.df_memory[feature_cols]
        self.y = self.df_memory["label"]
        self.sample_weight = self.df_memory["sample_weight"]

        self.X_text_train, self.X_text_test, self.X_num_train, self.X_num_test, self.y_train, self.y_test, self.sample_weight_train, self.sample_weight_test = train_test_split(
            self.X_text,
            self.X_num,
            self.y,
            self.sample_weight,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y
        )

        if self.retrain_pipe:
            self.df["sample_weight"] = 3.0
            self.X_text_train = pd.concat([self.X_text_train, self.df["text_preprocessed"]], ignore_index=True)
            self.X_num_train = pd.concat([self.X_num_train, self.df[feature_cols]],ignore_index=True)
            self.y_train = pd.concat([self.y_train, self.df["label"]], ignore_index=True)
            self.sample_weight_train = pd.concat([self.sample_weight_train, self.df["sample_weight"]], ignore_index=True)


    
    
    def tfidf_vectorization(self, artifact_path):
        """Cette méthode applique la vectorisation TF-IDF aux textes d'entraînement et de test.
        Elle utilise la classe TfidfVectorizer de scikit-learn pour transformer les textes en matrices de caractéristiques
        basées sur la fréquence des termes, puis retourne les matrices d'entraînement et de test.
        """
        if not self.prediction_pipe:
            vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=1, max_df=20_000_000)
            
            self.X_text_train_tfidf = vectorizer.fit_transform(self.X_text_train)
            self.X_text_test_tfidf = vectorizer.transform(self.X_text_test)
            logging.info("Enregistrement du nouvel artefact TF-IDF dans ML Flow")
            joblib.dump(vectorizer, f"{artifact_path}/tfidf.pkl")
            ML_Flow_Operations().save_model_artefact(f"{artifact_path}/tfidf.pkl")

        if self.prediction_pipe:
            logging.info("Réccupération du précédent artefact TF-IDF en local")
            vectorizer = joblib.load(f"{artifact_path}/tfidf.pkl")
            self.X_text_train_tfidf = vectorizer.transform(self.X_text_train)


          
    def dimension_reduction_truncated_SVD(self, artifact_path):
        if not self.prediction_pipe:
            svd = TruncatedSVD(
                n_components=300,
                random_state=42
            )

            self.X_text_train_svd = svd.fit_transform(self.X_text_train_tfidf)
            self.X_text_test_svd = svd.transform(self.X_text_test_tfidf)

            logging.info("Enregistrement du nouvel artefact SVD dans ML Flow")
            joblib.dump(svd, f"{artifact_path}/svd.pkl")
            ML_Flow_Operations().save_model_artefact(f"{artifact_path}/svd.pkl")

        if self.prediction_pipe:
            logging.info("Récupération du précédent artefact SVD en local")
            svd = joblib.load(f"{artifact_path}/svd.pkl")

            self.X_text_train_svd = svd.transform(self.X_text_train_tfidf)
            

    
    def robust_scale_numeric_features(self, artifact_path):
        """Cette méthode applique la normalisation robuste aux caractéristiques numériques d'entraînement et de test.
        Elle utilise la classe RobustScaler de scikit-learn pour transformer les caractéristiques numériques
        en utilisant la médiane et l'écart interquartile, puis retourne les matrices d'entraînement et de test normalisées.
        """
        if not self.prediction_pipe:
            scaler = RobustScaler()
            
            self.X_num_train_scaled = scaler.fit_transform(self.X_num_train)
            self.X_num_test_scaled = scaler.transform(self.X_num_test)
            logging.info("Enregistrement du nouvel artefact Robust Scaler dans ML Flow")
            joblib.dump(scaler, f"{artifact_path}/robust_scaler.pkl")
            ML_Flow_Operations().save_model_artefact(f"{artifact_path}/robust_scaler.pkl")

        if self.prediction_pipe:
            logging.info("Réccupération du précédent artefact Robust Scaler en local")
            scaler = joblib.load(f"{artifact_path}/robust_scaler.pkl")
            self.X_num_train_scaled = scaler.transform(self.X_num_train)

    
    def dimension_reduction_pca(self, artifact_path, explained_variance=0.99):
        """
        Réduit les dimensions des features numériques en conservant un pourcentage
        donné de la variance expliquée.
        """

        if not self.prediction_pipe:
            pca = PCA(
                n_components=explained_variance,
                random_state=42
            )

            self.X_num_train_pca = pca.fit_transform(self.X_num_train_scaled)
            self.X_num_test_pca = pca.transform(self.X_num_test_scaled)

            logging.info(
                f"PCA : {pca.n_components_} composantes conservées "
                f"({pca.explained_variance_ratio_.sum():.2%} de variance)"
            )

            logging.info(f"Enregistrement du nouvel artefact PCA en local : {artifact_path}")
            joblib.dump(pca, f"{artifact_path}/pca.pkl")
            logging.info("Enregistrement du nouvel artefact PCA dans ML Flow")
            ML_Flow_Operations().save_model_artefact(f"{artifact_path}/pca.pkl")

        else:
            logging.info("Récupération du précédent artefact PCA en local")
            pca = joblib.load(f"{artifact_path}/pca.pkl")

            self.X_num_train_pca = pca.transform(self.X_num_train_scaled)
            
    
    def hsstack_features(self):
        """Cette méthode combine les caractéristiques textuelles vectorisées et les caractéristiques numériques normalisées.
        Elle utilise la fonction hstack de scipy pour empiler horizontalement les matrices de caractéristiques
        et retourne les matrices d'entraînement et de test combinées.
        """
        if not self.prediction_pipe:
            self.X_train_combined = hstack([self.X_text_train_svd, self.X_num_train_pca]) 
            self.X_test_combined = hstack([self.X_text_test_svd, self.X_num_test_pca])

        if self.prediction_pipe:
            self.X_train_combined = hstack([self.X_text_train_svd, self.X_num_train_pca])

    
    def np_hsstack_features(self):
        if not self.prediction_pipe:
            self.X_train_combined = np.hstack([
                self.X_text_train_svd,
                self.X_num_train_pca
            ])

            self.X_test_combined = np.hstack([
                self.X_text_test_svd,
                self.X_num_test_pca
            ])

        if self.prediction_pipe:
            self.X_train_combined = np.hstack([
                self.X_text_train_svd,
                self.X_num_train_pca
            ])