import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import logging
import os

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MLFLOW_EXPERIMENT_NAME = "SpamShield"

_mlflow_configured = False


def _ensure_mlflow_configured():
    """Configure MLflow au premier vrai usage, pas au moment de l'import du module.
    Évite qu'un simple `import Model` (ou tout module qui en dépend) déclenche
    un appel réseau, ce qui casse les tests et les environnements sans MLflow actif."""
    global _mlflow_configured
    if not _mlflow_configured:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
        _mlflow_configured = True


class ML_Flow_Operations:
    def __init__(self):
        pass

    def save_metrics(self, metrics):
        _ensure_mlflow_configured()
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["precision"])
        mlflow.log_metric("recall", metrics["recall"])
        mlflow.log_metric("f1_score", metrics["f1_score"])
        mlflow.log_metric("training_nb", metrics["training_nb"])

    def save_model(self, model, model_name):
        _ensure_mlflow_configured()
        logging.info('Sauvegarde du model dans ML Flow')
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"SpamShieldClassifier-({model_name})")

    def save_model_artefact(self, pkl_path):
        _ensure_mlflow_configured()
        mlflow.log_artifact(pkl_path, artifact_path="artifacts")

    def get_latest_model(self):
        _ensure_mlflow_configured()
        client = MlflowClient()
        models = client.search_registered_models()
        models = sorted(models, key=lambda m: m.last_updated_timestamp, reverse=True)
        latest_model_name = models[0].name
        logging.info(f"Dernier modèle enregistré : {latest_model_name}")
        return mlflow.sklearn.load_model(f"models:/{latest_model_name}/latest")

    def get_latest_artefact(self, pkl_name):
        _ensure_mlflow_configured()
        runs = mlflow.search_runs(experiment_names=["SpamShield"], order_by=["start_time DESC"], max_results=1)
        if runs.empty:
            raise Exception("Aucun run MLflow trouvé.")
        run_id = runs.iloc[0]["run_id"]
        return mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=f"artifacts/{pkl_name}")

    def delete_all_models(self, model_name="SpamShieldClassifier"):
        _ensure_mlflow_configured()
        client = MlflowClient()
        versions = client.search_model_versions(f"name='{model_name}'")
        for v in versions:
            client.delete_model_version(name=model_name, version=v.version)
        try:
            client.delete_registered_model(model_name)
        except:
            pass
        logging.info(f"Tous les modèles et artefacts liés à '{model_name}' ont été supprimés.")

    def get_latest_model_metrics(self):
        _ensure_mlflow_configured()
        client = MlflowClient()
        models = client.search_registered_models()
        models = sorted(models, key=lambda m: m.last_updated_timestamp, reverse=True)
        latest_model = models[0]
        latest_model_name = latest_model.name
        versions = client.search_model_versions(f"name='{latest_model_name}'")
        versions = sorted(versions, key=lambda v: v.last_updated_timestamp, reverse=True)
        latest_version = versions[0]
        run_id = latest_version.run_id
        run = client.get_run(run_id)
        return run.data.metrics

    def log_llm_call(self, provider, model, tokens_in, tokens_out, duration, success, llm_response=None, payload=None, error=None):
        _ensure_mlflow_configured()
        with mlflow.start_run(run_name=f"llm_report_{provider}"):
            mlflow.set_tag("type", "llm_monitoring")
            mlflow.set_tag("provider", provider)
            mlflow.log_param("model", model)
            mlflow.log_metric("tokens_input", tokens_in or 0)
            mlflow.log_metric("tokens_output", tokens_out or 0)
            mlflow.log_metric("duration_seconds", duration)
            mlflow.log_metric("success", 1 if success else 0)
            if llm_response:
                mlflow.log_text(llm_response, "llm_response.txt")
            if payload:
                mlflow.log_dict(payload, "payload.json")
            if error:
                mlflow.log_param("error", str(error)[:250])
        logging.info(f"Appel LLM loggé dans MLflow : {provider}/{model} — succès={success}")

    def get_llm_monitoring_summary(self, limit=20):
        _ensure_mlflow_configured()
        runs = mlflow.search_runs(
            experiment_names=["SpamShield"],
            filter_string="tags.type = 'llm_monitoring'",
            order_by=["start_time DESC"],
            max_results=limit,
        )
        if runs.empty:
            return {"appels": [], "resume": []}
        colonnes = ["tags.provider", "params.model", "metrics.tokens_input",
                    "metrics.tokens_output", "metrics.duration_seconds",
                    "metrics.success", "start_time"]
        appels = runs[colonnes].to_dict(orient="records")
        resume = (
            runs.groupby("tags.provider")
            .agg(
                total_appels=("metrics.success", "count"),
                succes=("metrics.success", "sum"),
                tokens_total=("metrics.tokens_input", "sum"),
                latence_moyenne_s=("metrics.duration_seconds", "mean"),
            )
            .reset_index()
            .to_dict(orient="records")
        )
        return {"appels": appels, "resume": resume}