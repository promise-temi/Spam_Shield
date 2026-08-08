import time
import logging
from prometheus_client import Histogram, Counter

# Nombre de prédictions effectctuées

# ---------- Latence (couvre tout ce qui est déjà décoré par calculate_func_time) ----------
FUNCTION_DURATION = Histogram(
    "spamshield_function_duration_seconds",
    "Temps d'exécution des fonctions instrumentées par le décorateur calculate_func_time",
    ["function_name"],
)

# ---------- Volumétrie métier ----------
MESSAGES_TOTAL = Counter(
    "spamshield_messages_total",
    "Nombre total de messages traités, par décision finale",
    ["label"],  # "spam" ou "ham"
)

OVERRIDES_TOTAL = Counter(
    "spamshield_overrides_total",
    "Nombre de messages reclassés automatiquement par manque de confiance du modèle (seuil 60%)",
)

BUSINESS_RULES_TRIGGERED_TOTAL = Counter(
    "spamshield_business_rules_triggered_total",
    "Nombre de messages ayant déclenché au moins une règle métier",
)

GIBBERISH_DETECTED_TOTAL = Counter(
    "spamshield_gibberish_detected_total",
    "Nombre de messages détectés comme charabia par le modèle de Markov",
)


class Helpers_Monitoring:
    def __init__(self):
        pass

    def calculate_func_time(self, Methode_):
        """Décorateur qui mesure le temps d'exécution d'une fonction : le journalise
        dans les logs applicatifs (comportement d'origine, inchangé) ET l'enregistre
        comme métrique Prometheus, labellisée par le nom de la fonction. Un seul
        décorateur, déjà posé sur une vingtaine de méthodes du projet, suffit donc
        à obtenir la latence de tout le pipeline sans instrumenter chaque fichier
        individuellement."""
        def wrapper(*args, **kwargs):
            start = time.time()
            result = Methode_(*args, **kwargs)
            end = time.time()
            duration_seconds = end - start
            logging.info(f"{Methode_.__name__} : {duration_seconds / 60:.4f} minutes")
            FUNCTION_DURATION.labels(function_name=Methode_.__name__).observe(duration_seconds)
            return result
        return wrapper

    def record_message_outcome(self, final_label: bool, is_overridden: bool,
                                 business_rules_triggered: bool, gibberish_detected: bool):
        """Point d'entrée unique pour les métriques métier, appelé une seule fois par
        SpamShield_Operations.New_Message au moment où la décision finale est connue."""
        MESSAGES_TOTAL.labels(label="spam" if final_label else "ham").inc()
        if is_overridden:
            OVERRIDES_TOTAL.inc()
        if business_rules_triggered:
            BUSINESS_RULES_TRIGGERED_TOTAL.inc()
        if gibberish_detected:
            GIBBERISH_DETECTED_TOTAL.inc()