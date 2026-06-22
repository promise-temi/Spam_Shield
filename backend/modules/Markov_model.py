from collections import defaultdict, Counter
import re

class MarkovGibberishDetector:
    def __init__(self):
        self.transitions = defaultdict(Counter)
        self.total_counts = Counter()
        self.trained = False

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-zA-Zàâäéèêëîïôöùûüÿç ]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    # -----------------------------
    # ENTRAÎNEMENT
    # -----------------------------
    def train_model(self, tokens):
        text = " ".join(tokens)
        text = self.clean_text(text)

        for a, b in zip(text, text[1:]):
            self.transitions[a][b] += 1
            self.total_counts[a] += 1

        self.trained = True

    # -----------------------------
    # SCORE
    # -----------------------------
    def transition_probability(self, a, b):
        if self.total_counts[a] == 0:
            return 0
        return self.transitions[a][b] / self.total_counts[a]

    def markov_score(self, text):
        text = self.clean_text(text)
        if len(text) < 2:
            return 0

        probs = [self.transition_probability(a, b) for a, b in zip(text, text[1:])]
        self.score_ = sum(probs) / len(probs) if probs else 0
        return self.score_

    def is_gibberish(self, text, threshold=0.06):
        return self.markov_score(text) < threshold
