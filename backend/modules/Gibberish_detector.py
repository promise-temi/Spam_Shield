import re

class GibberishDetector:
    def __init__(self, corpus, markov_model):
        self.corpus = corpus
        self.markov = markov_model
        self.valid_chars = set("abcdefghijklmnopqrstuvwxyzàâäéèêëîïôöùûüÿç0123456789 .,!?;:'()-")

    def char_ratio(self, text):
        if not text:
            return 0
        valid = sum(1 for c in text.lower() if c in self.valid_chars)
        return valid / len(text)

    def word_ratio(self, text):
        words = re.findall(r"\b\w+\b", text.lower())
        if not words:
            return 0
        known = sum(1 for w in words if w in self.corpus)
        return known / len(words)

    def vowel_ratio(self, text):
        vowels = "aeiouyàâäéèêëîïôöùûüÿ"
        letters = [c for c in text.lower() if c.isalpha()]
        if not letters:
            return 0
        v = sum(1 for c in letters if c in vowels)
        return v / len(letters)

    def markov_score(self, text):
        return self.markov.score_text(text)

    def is_gibberish(self, text, threshold=0.45):
        score = (
            self.char_ratio(text) * 0.25 +
            self.word_ratio(text) * 0.25 +
            self.vowel_ratio(text) * 0.25 +
            self.markov_score(text) * 0.25
        )
        return score < threshold, score
