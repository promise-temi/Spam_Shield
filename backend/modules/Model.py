import os
import sys
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from xml.parsers.expat import model
from sklearn.svm import LinearSVC
from Gibberish_detector import GibberishDetector
from NLP_Feat_Eng import NLP_Feat_Eng
from Preprocessing import Preprocessing
from ML_Flow import ML_Flow_Operations

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
import joblib


class Model:
    def __init__(self, prediction_pipe=False):
        self.prediction_pipe = prediction_pipe

    def build_virgin_model_pipeline(self, X_train, X_test, y_train, y_test):
        """Cette méthode exécute l'ensemble du pipeline de construction d'un modèle vierge.
        Elle entraîne un modèle à partir des données d'entraînement, le teste sur les données de test,
        évalue les performances du modèle et sauvegarde le modèle entraîné.
        """
        model = self.train_model(X_train, y_train)
        y_pred = self.test_model(model, X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model_mlflow(model)
        return evaluation_results
    
    def AI_full_virgin_model_training_pipeline(self, df, corpus_path):
        """Cette méthode exécute l'ensemble du pipeline de construction d'un modèle vierge à partir d'un DataFrame.
            Elle effectue l'ingénierie des caractéristiques NLP sur le DataFrame, puis exécute le pipeline de prétraitement
            pour préparer les données d'entraînement et de test, et enfin exécute le pipeline de construction du modèle vierge
            pour entraîner, tester, évaluer et sauvegarder le modèle.
            """
        logging.info("Début du pipeline de création d'un model de prédiction vierge")
        if df.shape[0] < 10:
            raise ValueError("Le DataFrame doit contenir au moins 10 lignes pour entraîner un modèle.")
        features = NLP_Feat_Eng(df, corpus_path).feature_engineering_full_pipeline()
        X_train, X_test, y_train, y_test = Preprocessing(features).preprocessing_pipeline()
        metrics = Model().build_virgin_model_pipeline(X_train, X_test, y_train, y_test)
        logging.info("Fin du pipeline - Enregistrement du model dans ML Flow")
        ML_Flow_Operations().save_metrics(metrics)
    

    def AI_full_retrain_model_pipeline(self, df, corpus_path):
        logging.info("Début du pipeline de réentraînement d'un model de prédiction existant")
        if df.shape[0] < 10:
            raise ValueError("Le DataFrame doit contenir au moins 10 lignes pour ré-entraîner un modèle.")
        features = NLP_Feat_Eng(df, corpus_path).feature_engineering_full_pipeline()
        X_train, X_test, y_train, y_test = Preprocessing(features).preprocessing_pipeline()
        metrics = Model().__retrain_model_pipeline(X_train, X_test, y_train, y_test)
        logging.info("Fin du pipeline - Enregistrement du model dans ML Flow")
        ML_Flow_Operations().save_metrics(metrics)

    def __retrain_model_pipeline(self, X_train, X_test, y_train, y_test):
        """Cette méthode exécute l'ensemble du pipeline de rechargement d'un modèle existant.
        Elle charge un modèle existant, le réentraîne sur les nouvelles données d'entraînement,
        le teste sur les données de test, évalue les performances du modèle et sauvegarde le modèle mis à jour.
        """
        model = ML_Flow_Operations().get_latest_model()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model_mlflow(model)
        return evaluation_results
        
    def AI_full_prediction_pipeline(self, df, corpus_path):
        features = NLP_Feat_Eng(df, corpus_path).feature_engineering_full_pipeline()
        X = Preprocessing(features, self.prediction_pipe).preprocessing_pipeline()
        y_pred = self.predict(X)
        return y_pred

    def train_model(self, X_train, y_train):
        """Cette méthode entraîne un modèle de classification à partir des données d'entraînement.
        Elle utilise un classificateur linéaire SVM pour apprendre à partir des caractéristiques d'entrée et des étiquettes de classe.
        """
        model= LinearSVC(max_iter=10000)
        model.fit(X_train, y_train)
        return model

    
    def test_model(self, model, X_test):
        """Cette méthode teste un modèle entraîné sur les données de test.
        Elle utilise le modèle pour faire des prédictions sur les caractéristiques de 
        test et retourne les étiquettes prédites.
        """
        y_pred = model.predict(X_test)
        return y_pred
    
    def evaluate_model(self, y_test, y_pred):
        """Cette méthode évalue les performances d'un modèle en comparant les 
        étiquettes de test réelles avec les étiquettes prédites.
        Elle calcule plusieurs métriques d'évaluation, telles que l'accuracy, 
        la précision, le rappel, le F1-score, la matrice de confusion et le rapport de classification,
        et retourne ces métriques dans un dictionnaire.
        """
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        conf_matrix = confusion_matrix(y_test, y_pred)
        class_report = classification_report(y_test, y_pred)

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "confusion_matrix": conf_matrix,
            "classification_report": class_report
        }
    
    def save_model_mlflow(self, model):
        ML_Flow_Operations().save_model(model)
    
    def save_model_local(self, model, file_path):
        joblib.dump(model, file_path)


    def predict(self, X):
        """Cette méthode charge un modèle à partir d'un chemin de fichier spécifié et utilise ce modèle pour faire des prédictions sur les données d'entrée.
        Elle retourne les étiquettes prédites par le modèle.
        """
        model = ML_Flow_Operations().get_latest_model()
        y_pred = model.predict(X)
        return y_pred