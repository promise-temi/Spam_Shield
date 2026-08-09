import time
import logging
from prometheus_client import Histogram, Counter

FUNCTION_DURATION = Histogram(
    "spamshield_function_duration_seconds",
    "Temps d'exécution des fonctions instrumentées par le décorateur calculate_func_time",
    ["function_name"],
)

FUNCTION_RESULT = Counter(
    "spamshield_function_result_total",
    "Résultat d'exécution des fonctions",
    ["pipe_type", "function_name", "status", "error_type"],
)

PREDICTION_COUNTER = Counter(
    "spamshield_predictions_total",
    "Nombre de prédictions effectuées",
    ["final_label", "model_pred", "business_rules_triggered", "is_overridden"]
)

CONFIDENCE_HISTOGRAM = Histogram(
    "spamshield_confidence_score",
    "Distribution du score de confiance du modèle",
    ["final_label"],
    buckets=[0.5, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99]
)

GIBBERISH_SCORE_HISTOGRAM = Histogram(
    "spamshield_gibberish_score",
    "Distribution du score de charabia détecté par les règles métier",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

BANNED_PATTERNS_COUNTER = Counter(
    "spamshield_banned_patterns_total",
    "Patterns interdits et anomalies détectés par les règles métier",
    ["anomaly_type"]
)

HTTP_ERRORS_COUNTER = Counter(
    "spamshield_http_errors_total",
    "Erreurs HTTP par endpoint et code de statut",
    ["endpoint", "method", "status_code"]
)

UNAUTHORIZED_COUNTER = Counter(
    "spamshield_unauthorized_attempts_total",
    "Tentatives d'accès non autorisées (clé API invalide ou manquante)",
    ["endpoint", "method"]
)


class Helpers_Monitoring:
    def __init__(self):
        pass

    def calculate_func_time(self, Methode_):
        """Décorateur qui mesure le temps d'exécution d'une fonction."""
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = Methode_(*args, **kwargs)
                return result
            except Exception as e:
                raise e
            finally:
                duration_seconds = time.time() - start
                logging.info(f"{Methode_.__name__} : {duration_seconds / 60:.4f} minutes")
                FUNCTION_DURATION.labels(function_name=Methode_.__name__).observe(duration_seconds)
        return wrapper

    def record_methode_result(self, pipe_type, is_success, name, status, error_type=None):
        """Enregistre le résultat d'exécution d'une méthode dans Prometheus."""
        if is_success:
            FUNCTION_RESULT.labels(pipe_type=pipe_type, function_name=name, status=status, error_type="none").inc()
        else:
            FUNCTION_RESULT.labels(pipe_type=pipe_type, function_name=name, status=status, error_type=type(error_type).__name__).inc()

    def record_prediction(self, final_label, model_pred, business_rules_triggered, is_overridden, confidence_score):
        """Enregistre les compteurs de prédictions + distribution du score de confiance."""
        label_str = "spam" if final_label == 1 else "ham"

        PREDICTION_COUNTER.labels(
            final_label=label_str,
            model_pred="spam" if model_pred else "ham",
            business_rules_triggered=str(bool(business_rules_triggered)),
            is_overridden=str(bool(is_overridden))
        ).inc()

        CONFIDENCE_HISTOGRAM.labels(
            final_label=label_str
        ).observe(float(confidence_score))

    def record_gibberish(self, gibberish_score):
        """Enregistre le score de charabia du modèle de Markov."""
        if gibberish_score is not None:
            GIBBERISH_SCORE_HISTOGRAM.observe(float(gibberish_score))

    def record_banned_patterns(self, banned_patterns_found):
        """Enregistre les anomalies détectées par les règles métier."""
        if banned_patterns_found:
            for pattern in banned_patterns_found:
                anomaly = str(pattern).strip()[:50]
                BANNED_PATTERNS_COUNTER.labels(anomaly_type=anomaly).inc()

    def record_label_correction(self):
        """Enregistre une correction humaine du label d'un message."""
        FUNCTION_RESULT.labels(
            pipe_type="Human Feedback",
            function_name="Label Correction",
            status="success",
            error_type="none"
        ).inc()

    def record_model_retrain(self, is_success, error_type=None):
        """Enregistre un réentraînement du modèle."""
        if is_success:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Model Retrain",
                status="success",
                error_type="none"
            ).inc()
        else:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Model Retrain",
                status="failure",
                error_type=type(error_type).__name__
            ).inc()

    def record_virgin_model_training(self, is_success, error_type=None):
        """Enregistre un entraînement de modèle vierge."""
        if is_success:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Virgin Model Training",
                status="success",
                error_type="none"
            ).inc()
        else:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Virgin Model Training",
                status="failure",
                error_type=type(error_type).__name__
            ).inc()

    def record_model_existence_check(self, is_success, model_found=None, error_type=None):
        """Enregistre la vérification d'existence du modèle dans MLflow."""
        if is_success:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Check Model Existence",
                status="success",
                error_type="none"
            ).inc()
        else:
            FUNCTION_RESULT.labels(
                pipe_type="ML Pipeline",
                function_name="Check Model Existence",
                status="failure",
                error_type=type(error_type).__name__
            ).inc()

    def record_http_error(self, endpoint, method, status_code):
        """Enregistre une erreur HTTP par endpoint et code de statut."""
        HTTP_ERRORS_COUNTER.labels(
            endpoint=endpoint,
            method=method,
            status_code=str(status_code)
        ).inc()

    def record_unauthorized_attempt(self, endpoint, method):
        """Enregistre une tentative d'accès non autorisée."""
        UNAUTHORIZED_COUNTER.labels(
            endpoint=endpoint,
            method=method
        ).inc()