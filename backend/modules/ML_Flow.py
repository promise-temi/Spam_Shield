import mlflow
import os
import mlflow.sklearn
from mlflow.tracking import MlflowClient 
import logging


mlflow.set_tracking_uri(
    os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5050")
)

mlflow.set_experiment("SpamShield")





class ML_Flow_Operations:
    def __init__(self):
        pass

    def save_metrics(self, metrics):
        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["precision"])
        mlflow.log_metric("recall", metrics["recall"])
        mlflow.log_metric("f1_score", metrics["f1_score"])
        mlflow.log_metric("training_nb", metrics["training_nb"])

    def save_model(self, model, model_name):
        logging.info('Sauvegarde du model dans ML Flow')
        mlflow.set_tag("type", "pred_model")
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"SpamShieldClassifier-({model_name})")

    def save_model_artefact(self, pkl_path):
        mlflow.log_artifact(pkl_path, artifact_path="artifacts")

    def get_latest_pred_model_run(self):
        runs = mlflow.search_runs(
            experiment_names=["SpamShield"],
            filter_string="tags.type = 'pred_model'",
            order_by=["start_time DESC"],
            max_results=1
        )

        if runs.empty:
            return None

        return runs.iloc[0]

    def get_latest_model(self):
        run = self.get_latest_pred_model_run()

        if run is None:
            logging.info("Aucun modèle SpamShield trouvé dans MLflow.")
            return None

        run_id = run["run_id"]

        logging.info(
            f"Chargement du modèle depuis le run : {run_id}"
        )

        return mlflow.sklearn.load_model(
            f"runs:/{run_id}/model"
        )

    def get_latest_artefact(self, pkl_name):
        run = self.get_latest_pred_model_run()

        if run is None:
            raise Exception("Aucun run de modèle trouvé dans MLflow.")

        run_id = run["run_id"]

        return mlflow.artifacts.download_artifacts(
            run_id=run_id,
            artifact_path=f"artifacts/{pkl_name}"
        )

    def delete_all_models(self, model_name="SpamShieldClassifier"):
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
        run = self.get_latest_pred_model_run()

        if run is None:
            raise Exception("Aucun run de modèle trouvé dans MLflow.")

        client = MlflowClient()
        run_data = client.get_run(run["run_id"])

        return run_data.data.metrics

    def log_llm_call(self, provider, model, tokens_in, tokens_out, duration, success, llm_response=None, payload=None, error=None):
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


    
































# import mlflow
# import os
# import mlflow.sklearn
# from mlflow.tracking import MlflowClient 
# import logging


# mlflow.set_tracking_uri(
#     os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5050")
# )

# mlflow.set_experiment("SpamShield")

# class ML_Flow_Operations:
#     def __init__(self):
#         pass

#     def save_metrics(self, metrics):
#         # Cette methode logs les metriques d'un modèle dans mlflow
#         mlflow.log_metric("accuracy", metrics["accuracy"])
#         mlflow.log_metric("precision", metrics["precision"])
#         mlflow.log_metric("recall", metrics["recall"])
#         mlflow.log_metric("f1_score", metrics["f1_score"])
#         mlflow.log_metric("training_nb", metrics["training_nb"])

#     def save_model(self, model, model_name):
#         logging.info('Sauvegarde du model dans ML Flow')
#         mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"SpamShieldClassifier-({model_name})")

#     def save_model_artefact(self, pkl_path):
#         mlflow.log_artifact(pkl_path, artifact_path="artifacts")

    
#     def get_latest_training_run(self):
#         runs = mlflow.search_runs(
#             experiment_names=["SpamShield"],
#             order_by=["start_time DESC"]
#         )

#         if runs.empty:
#             return None

#         runs = runs[
#             runs["tags.mlflow.runName"].isin([
#                 "model_vierge",
#                 "retrain_model"
#             ])
#         ]

#         if runs.empty:
#             return None

#         return runs.iloc[0]


#     def get_latest_model_metrics(self):
#         run = self.get_latest_training_run()

#         if run is None:
#             raise Exception(
#                 "Aucun run d'entraînement trouvé dans MLflow."
#             )

#         run_id = run["run_id"]

#         client = MlflowClient()
#         run_data = client.get_run(run_id)

#         return run_data.data.metrics

#     def get_latest_artefact(self, pkl_name):
#         runs = mlflow.search_runs(
#             experiment_names=["SpamShield"],
#             filter_string=(
#                 "tags.`mlflow.runName` = 'model_vierge' "
#                 "OR tags.`mlflow.runName` = 'retrain_model'"
#             ),
#             order_by=["start_time DESC"],
#             max_results=1
#         )

#         if runs.empty:
#             raise Exception(
#                 "Aucun run d'entraînement trouvé dans MLflow."
#             )

#         run_id = runs.iloc[0]["run_id"]

#         logging.info(
#             f"Récupération de l'artefact {pkl_name} "
#             f"depuis le run {run_id}"
#         )

#         return mlflow.artifacts.download_artifacts(
#             run_id=run_id,
#             artifact_path=f"artifacts/{pkl_name}"
#         )
   

#     def delete_all_models(self):
#         client = MlflowClient()

#         models = client.search_registered_models()

#         models = [
#             model
#             for model in models
#             if model.name.startswith("SpamShieldClassifier")
#         ]

#         if not models:
#             logging.info("Aucun modèle SpamShield à supprimer.")
#             return

#         for model in models:
#             versions = client.search_model_versions(
#                 f"name='{model.name}'"
#             )

#             for version in versions:
#                 client.delete_model_version(
#                     name=model.name,
#                     version=version.version
#                 )

#             client.delete_registered_model(
#                 model.name
#             )

#             logging.info(
#                 f"Modèle supprimé : {model.name}"
#             )

#         logging.info(
#             "Tous les modèles SpamShield ont été supprimés du registry."
#         )

        
#     from mlflow.tracking import MlflowClient

#     def get_latest_model_metrics(self):
        
#         runs = mlflow.search_runs(
#             experiment_names=["SpamShield"],
#             filter_string=(
#                 "tags.`mlflow.runName` = 'model_vierge' "
#                 "OR tags.`mlflow.runName` = 'retrain_model'"
#             ),
#             order_by=["start_time DESC"],
#             max_results=1
#         )

#         if runs.empty:
#             raise Exception(
#                 "Aucun run d'entraînement trouvé dans MLflow."
#             )

#         run_id = runs.iloc[0]["run_id"]

#         client = MlflowClient()
#         run = client.get_run(run_id)

#         return run.data.metrics

#     def log_llm_call(self, provider, model, tokens_in, tokens_out, duration, success, llm_response=None, payload=None, error=None):
#         """Journalise un appel au service de génération de rapport (Mistral/Gemini) dans MLflow."""
#         with mlflow.start_run(run_name=f"llm_report_{provider}"):
#             mlflow.set_tag("type", "llm_monitoring")
#             mlflow.set_tag("provider", provider)
#             mlflow.log_param("model", model)
#             mlflow.log_metric("tokens_input", tokens_in or 0)
#             mlflow.log_metric("tokens_output", tokens_out or 0)
#             mlflow.log_metric("duration_seconds", duration)
#             mlflow.log_metric("success", 1 if success else 0)

#             if llm_response:
#                 mlflow.log_text(llm_response, "llm_response.txt")

#             if payload:
#                 mlflow.log_dict(payload, "payload.json")

#             if error:
#                 mlflow.log_param("error", str(error)[:250])
#         logging.info(f"Appel LLM loggé dans MLflow : {provider}/{model} — succès={success}")

        
#     def get_llm_monitoring_summary(self, limit=20):
#         """Retourne les derniers appels LLM et un cumul par fournisseur (tokens, latence, taux d'échec)."""
#         runs = mlflow.search_runs(
#             experiment_names=["SpamShield"],
#             filter_string="tags.type = 'llm_monitoring'",
#             order_by=["start_time DESC"],
#             max_results=limit,
#         )
#         if runs.empty:
#             return {"appels": [], "resume": []}

#         colonnes = ["tags.provider", "params.model", "metrics.tokens_input",
#                     "metrics.tokens_output", "metrics.duration_seconds",
#                     "metrics.success", "start_time"]
#         appels = runs[colonnes].to_dict(orient="records")

#         resume = (
#             runs.groupby("tags.provider")
#             .agg(
#                 total_appels=("metrics.success", "count"),
#                 succes=("metrics.success", "sum"),
#                 tokens_total=("metrics.tokens_input", "sum"),
#                 latence_moyenne_s=("metrics.duration_seconds", "mean"),
#             )
#             .reset_index()
#             .to_dict(orient="records")
#         )

#         return {"appels": appels, "resume": resume}