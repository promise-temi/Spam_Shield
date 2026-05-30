from collections import defaultdict, Counter
import re

class MarkovModel:
    def __init__(self):
        self.transitions = defaultdict(Counter)
        self.total_counts = Counter()

    def train(self, texts):
        for text in texts:
            text = re.sub(r"[^a-zA-Zàâäéèêëîïôöùûüÿç]", "", text.lower())
            for a, b in zip(text, text[1:]):
                self.transitions[a][b] += 1
                self.total_counts[a] += 1

    def transition_prob(self, a, b):
        if self.total_counts[a] == 0:
            return 0
        return self.transitions[a][b] / self.total_counts[a]

    def score_text(self, text):
        text = re.sub(r"[^a-zA-Zàâäéèêëîïôöùûüÿç]", "", text.lower())
        if len(text) < 2:
            return 0

        probs = []
        for a, b in zip(text, text[1:]):
            probs.append(self.transition_prob(a, b))

        if not probs:
            return 0

        return sum(probs) / len(probs)
