import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient 
import logging


mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)

mlflow.set_experiment("SpamShield")

class ML_Flow_Operations:
    def __init__(self):
        pass

    def save_metrics(self, metrics):
        # Cette methode logs les metriques d'un modèle dans mlflow
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["precision"])
        mlflow.log_metric("recall", metrics["recall"])
        mlflow.log_metric("f1_score", metrics["f1_score"])
        mlflow.log_metric("training_nb", metrics["training_nb"])

    def save_model(self, model, model_name):
        logging.info('Sauvegarde du model dans ML Flow')
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"SpamShieldClassifier-({model_name})")

    def save_model_artefact(self, pkl_path):
        mlflow.log_artifact(pkl_path, artifact_path="artifacts")

    
    # def get_latest_model(self):
    #     return mlflow.sklearn.load_model("models:/SpamShieldClassifier/latest")
    
    def get_latest_model(self):
        client = MlflowClient()
        models = client.search_registered_models()
        models = sorted(models, key=lambda m: m.last_updated_timestamp, reverse=True)
        latest_model_name = models[0].name
        logging.info("Dernier modèle enregistré :", latest_model_name)
        return mlflow.sklearn.load_model(f"models:/{latest_model_name}/latest")
    
    def get_latest_artefact(self, pkl_name):
        runs = mlflow.search_runs(experiment_names=["SpamShield"], order_by=["start_time DESC"], max_results=1)

        if runs.empty:
            raise Exception("Aucun run MLflow trouvé.")
        run_id = runs.iloc[0]["run_id"] 

        return mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=f"artifacts/{pkl_name}")
    

   

    def delete_all_models(self, model_name="SpamShieldClassifier"):
        client = MlflowClient()

        # Supprimer toutes les versions du modèle
        versions = client.search_model_versions(f"name='{model_name}'")
        for v in versions:
            client.delete_model_version(name=model_name, version=v.version)

        # Supprimer le modèle du registry
        try:
            client.delete_registered_model(model_name)
        except:
            pass

        logging.info(f"Tous les modèles et artefacts liés à '{model_name}' ont été supprimés.")
