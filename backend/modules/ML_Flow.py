import mlflow
import mlflow.sklearn
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

    def save_model(self, model):
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name="SpamShieldClassifier")

    def save_model_artefact(self, pkl_path):
        mlflow.log_artifact(pkl_path, artifact_path="artifacts")

    
    def get_latest_model(self):
        return mlflow.sklearn.load_model("models:/SpamShieldClassifier/1")
    
    def get_latest_artefact(self, pkl_path):
        runs = mlflow.search_runs(order_by=["start_time DESC"], max_results=1)
        run_id = runs.iloc[0]["run_id"]
        return mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=pkl_path)

