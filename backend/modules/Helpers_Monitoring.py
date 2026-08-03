import time
import logging
# from prometheus_client import Histogram

# API_DURATION = Histogram(
#     "api_duration_seconds",
#     "Temps des routes API (fonctionalitées complètes)"
# )

# PIPELINE_DURATION = Histogram(
#     "pipeline_duration_seconds",
#     "Temps des pipelines"
# )

# PREPROCESSING_DURATION = Histogram(
#     "preprocessing_duration_seconds",
#     "Temps des methodes de proprocessing"
# )

# FEAT_ENG_DURATION = Histogram(
#     "feat_eng_duration_seconds",
#     "Temps des methodes de feature engineering"
# )

# MODEL_INFERANCE_DURATION = Histogram(
#     "feat_eng_duration_seconds",
#     "Temps des methodes de feature engineering"
# )

class Helpers_Monitoring:
    def __init__(self):
        pass

    def calculate_func_time(self, Methode_):
        """Cette méthode est un décorateur qui mesure le temps d'exécution d'une fonction et logge ce temps avec le nom de la fonction.
        Elle prend en argument une fonction (Methode_) et retourne une nouvelle fonction (wrapper)
        qui exécute la fonction d'origine, mesure le temps d'exécution et logge le résultat.
        """
        def wrapper(*args, **kwargs):
            start = time.time()
            result = Methode_(*args, **kwargs)   # <-- tu EXÉCUTES la fonction
            end = time.time()
            total_time = (end - start) / 60 # en minutes
            logging.info(f"{Methode_.__name__} : {total_time:.4f} minutes")
            return result                        # <-- tu renvoies le résultat
        return wrapper
