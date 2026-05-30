from xml.parsers.expat import model
from sklearn.svm import LinearSVC
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
    def __init__(self):
        pass

    def build_virgin_model_pipeline(self, X_train, y_train, X_test, y_test, model_path):
        """Cette méthode exécute l'ensemble du pipeline de construction d'un modèle vierge.
        Elle entraîne un modèle à partir des données d'entraînement, le teste sur les données de test,
        évalue les performances du modèle et sauvegarde le modèle entraîné.
        """
        model = self.train_model(X_train, y_train)
        y_pred = self.test_model(model, X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model(model, model_path)
        return evaluation_results
    

    def retrain_model_pipeline(self, X_train, y_train, X_test, y_test, model_path):
        """Cette méthode exécute l'ensemble du pipeline de rechargement d'un modèle existant.
        Elle charge un modèle existant, le réentraîne sur les nouvelles données d'entraînement,
        le teste sur les données de test, évalue les performances du modèle et sauvegarde le modèle mis à jour.
        """
        model = joblib.load(model_path)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        evaluation_results = self.evaluate_model(y_test, y_pred)
        self.save_model(model, model_path)
        return evaluation_results
        

    def train_model(self, X_train, y_train):
        """Cette méthode entraîne un modèle de classification à partir des données d'entraînement.
        Elle utilise un classificateur linéaire SVM pour apprendre à partir des caractéristiques d'entrée et des étiquettes de classe.
        """
        model= LinearSVC()
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
    
    def save_model(self, model, file_path):
        joblib.dump(model, file_path)


    def predict(self, model_path, X):
        """Cette méthode charge un modèle à partir d'un chemin de fichier spécifié et utilise ce modèle pour faire des prédictions sur les données d'entrée.
        Elle retourne les étiquettes prédites par le modèle.
        """
        model = joblib.load(model_path)
        y_pred = model.predict(X)
        return y_pred