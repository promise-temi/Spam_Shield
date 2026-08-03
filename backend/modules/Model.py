import os
import sys
import logging
import mlflow
import numpy as np
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from sklearn.svm import LinearSVC
from NLP_Feat_Eng import NLP_Feat_Eng
from Preprocessing import Preprocessing
from ML_Flow import ML_Flow_Operations
from Set_SpamShield import SET_Spam_Shield_Dependances


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
    def __init__(self, prediction_pipe=False, model=LinearSVC(max_iter=20000, random_state=42), model_name="LinearSVC", metadata={}, seuil_confiance=True):
        self.prediction_pipe = prediction_pipe
        self.corpus_path = f"{os.path.dirname(__file__)}/data/corpus.parquet"
        self.artifact_path = f"{os.path.dirname(__file__)}/data"
        self.model = model
        self.model_name = model_name
        self.metadata = metadata
        self.seuil_confiance = seuil_confiance
        self.override = False

    def build_virgin_model_pipeline(self, X_train, X_test, y_train, y_test):
        """Cette méthode exécute l'ensemble du pipeline de construction d'un modèle vierge.
        Elle entraîne un modèle à partir des données d'entraînement, le teste sur les données de test,
        évalue les performances du modèle et sauvegarde le modèle entraîné.
        """
        model = self.train_model(X_train, y_train)
        y_pred = self.test_model(model, X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model_mlflow(model, self.model_name)
        self.save_model_local(model, f"{self.artifact_path}/model.pkl")
        return evaluation_results
    
    def AI_full_virgin_model_training_pipeline(self):
        """Cette méthode exécute l'ensemble du pipeline de construction d'un modèle vierge à partir d'un DataFrame.
            Elle effectue l'ingénierie des caractéristiques NLP sur le DataFrame, puis exécute le pipeline de prétraitement
            pour préparer les données d'entraînement et de test, et enfin exécute le pipeline de construction du modèle vierge
            pour entraîner, tester, évaluer et sauvegarder le modèle.
            """
        logging.info("Début du pipeline de création d'un model de prédiction vierge")
        self.training_data = SET_Spam_Shield_Dependances(raw_data_dir=f"{os.path.dirname(__file__)}/data/raw_data/").Dependances_Full_Pipeline(lang='fr')
        if self.training_data.shape[0] < 10:
            raise ValueError("Le DataFrame doit contenir au moins 10 lignes pour entraîner un modèle.")
        # ML_Flow_Operations().delete_all_models()
        with mlflow.start_run(run_name="model_vierge"):
            features = NLP_Feat_Eng(self.training_data, self.corpus_path).feature_engineering_full_pipeline()
            preprocessing = Preprocessing(features, self.artifact_path)
            preprocessing.delete_memory_data()
            X_train, X_test, y_train, y_test, _, __ = preprocessing.preprocessing_pipeline()
            self.X_train = X_train
            metrics = self.build_virgin_model_pipeline(X_train, X_test, y_train, y_test)
            logging.info("Fin du pipeline - Enregistrement du model dans ML Flow")
            ML_Flow_Operations().save_metrics(metrics)
    

    def AI_full_retrain_model_pipeline(self, df, ):
        logging.info("Début du pipeline de réentraînement d'un model de prédiction existant")
        if df.shape[0] < 10:
            raise ValueError("Le DataFrame doit contenir au moins 10 lignes pour ré-entraîner un modèle.")
        with mlflow.start_run(run_name="retrain_model"):
            features = NLP_Feat_Eng(df, self.corpus_path).feature_engineering_full_pipeline()
            X_train, X_test, y_train, y_test, s_weight_train, _ = Preprocessing(features, self.artifact_path).preprocessing_pipeline()
            self.X_train = X_train
            metrics = self.__retrain_model_pipeline(X_train, X_test, y_train, y_test, s_weight_train)
            logging.info("Fin du pipeline - Enregistrement du model dans ML Flow")  
            ML_Flow_Operations().save_metrics(metrics)

    def __retrain_model_pipeline(self, X_train, X_test, y_train, y_test, s_weight_train):
        """Cette méthode exécute l'ensemble du pipeline de rechargement d'un modèle existant.
        Elle charge un modèle existant, le réentraîne sur les nouvelles données d'entraînement,
        le teste sur les données de test, évalue les performances du modèle et sauvegarde le modèle mis à jour.
        """
        model = ML_Flow_Operations().get_latest_model()
        model.fit(X_train, y_train, sample_weight=s_weight_train)
        y_pred = model.predict(X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model_mlflow(model, f"RETRAIN - {self.model_name}")
        self.save_model_local(model, f"{self.artifact_path}/model.pkl")
        return evaluation_results
        
    def AI_full_prediction_pipeline(self, df):
        self.features = NLP_Feat_Eng(df, self.corpus_path, self.metadata, self.prediction_pipe).feature_engineering_full_pipeline()
        X = Preprocessing(self.features, self.artifact_path, self.prediction_pipe).preprocessing_pipeline()
        y_pred = self.predict(X)
        return y_pred

    def train_model(self, X_train, y_train):
        """Cette méthode entraîne un modèle de classification à partir des données d'entraînement.
        Elle utilise un classificateur linéaire SVM pour apprendre à partir des caractéristiques d'entrée et des étiquettes de classe.
        """
        model= self.model
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
            "training_nb": int(self.X_train.shape[0]),
            "confusion_matrix": conf_matrix,
            "classification_report": class_report
        }
    
    
    def save_model_mlflow(self, model, model_name):
        ML_Flow_Operations().save_model(model, model_name)
    
    def save_model_local(self, model, file_path):
        joblib.dump(model, file_path)


    def predict(self, X):
        """Cette méthode charge un modèle à partir d'un chemin de fichier spécifié et utilise ce modèle pour faire des prédictions sur les données d'entrée.
        Elle retourne les étiquettes prédites par le modèle.
        """
        # model = ML_Flow_Operations().get_latest_model()
        model = joblib.load( f"{self.artifact_path}/model.pkl")
        y_pred = model.predict(X)
        self.get_confidence(model, X)
        if self.seuil_confiance:
            final_pred = self.confidence_based_pred(y_pred, self.confidence_score)
            return final_pred
        else:
            return y_pred
    
    def get_confidence(self, model, X):
        scores = model.decision_function(X)
        confidence = 1 / (1 + np.exp(-np.abs(scores)))
        self.confidence_score = float(confidence[0])

    def confidence_based_pred(self, pred, confidence):
        if pred[0] == 0 and confidence <= 0.60:
            pred[0] = not pred[0]
            self.override = True
            return pred
        else:
            return pred


