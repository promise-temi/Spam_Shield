import time
import logging
from prometheus_client import Histogram, Counter, REGISTRY, Gauge

def _get_or_create(cls, name, doc, labelnames=[], **kwargs):
    """Récupère une métrique existante ou en crée une nouvelle — évite le crash au reload uvicorn."""
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return cls(name, doc, labelnames, **kwargs)



class Helpers_Monitoring:
    def __init__(self):
        # Métriques pour le suivi des prédictions
        self.MODEL_PREDICTION_INFERENCE = _get_or_create(
            Gauge, 
            "model_pred_inference", 
            "Temps d'inférence à un instant T"
        )

        self.TOTAL_SPAM_PREDICTIONS = _get_or_create(
            Counter,
            "spam_Total_predictions",
            "Total des messages SPAMS",
            ['Model', 'B_Rules']
        )

        self.TOTAL_HAM_PREDICTIONS = _get_or_create(
            Counter,
            "ham_Total_predictions",
            "Total des messages HAM"
        )

        self.CONFIDENCE_SCORE = _get_or_create(
            Gauge,
            "Confidence_score",
            "Score de confiance à un instant T"
        )

        self.TOTAL_MESSAGE = _get_or_create(
            Counter,
            "Total_Messages",
            "Nombre total de messages recu officielement"
        )

        self.MESSAGE_FAILS = _get_or_create(
            Gauge,
            "Total_Messages_fails",
            "Nombre total de pipeline de mesages échouée"
        )

        # Métriques pour le suivi du model lors de l'entrainement et réentrainement
        self.CHECK_MODEL_EXISTANCE_FAILS = _get_or_create(
            Gauge,
            "check_model_existance",
            "Nombre total de fois ou l'existance du model à été vérifiée à un instant T et a été un echec"
        )

        self.RETRAIN_PIPELINE_FAILS = _get_or_create(
            Gauge,
            "retrain_pipeline_fails",
            "Nombre total de fois ou le réentrainement à échoué à un instant T"
        )

        self.INITIAL_TRAIN_FAILS = _get_or_create(
            Gauge,
            "train_pipeline_fails",
            "Nombre total de fois ou l'entrainement à échoué à un instant T"
        )

        self.TOTAL_INITIAL_TRAINS = _get_or_create(
            Counter,
            'initial_trains_total',
            'Nombre total de fois où il y a eu un entrainement de model vierge'
        )

        self.TOTAL_RETRAINS = _get_or_create(
            Counter,
            'retrains_total',
            'Nombre total de réentrainements'
        )

        self.TOTAL_LLM_CALLS = _get_or_create(
            Counter,
            'llm_calls_total',
            'Nombre total d appel llm'
        )

        self.TOTAL_LLM_CALLS_FAILS = _get_or_create(
            Gauge,
            'llm_call_fail',
            'Nombre de fois ou le llm à échoué'
        )

        self.FLUSH_MESSAGES_FAIL = _get_or_create(
            Gauge,
            'forced_new_phase_fail',
            'La fonctionalité de flush a échoué ou non'
        )

        # monitoring API
        self.UNAUTHORIZED = _get_or_create(
            Counter,
            'unauthorized_access_tentative',
            'Session expiré, clé API invalide'
        )

        self.FORBIDEN = _get_or_create(
            Counter,
            'forbidden_user_tentative',
            'Utilisateur non autorisé à acceder a une ressources, identifié mais accès interdit'
        )



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
        return wrapper

