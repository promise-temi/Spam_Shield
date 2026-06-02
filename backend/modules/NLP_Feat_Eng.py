
import re
import numpy as np
import pandas as pd
import os
import logging
import time
import sys
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Helpers_Monitoring import Helpers_Monitoring
monitor = Helpers_Monitoring()


urgency_words = [
    "urgent", "immédiat", "immédiate", "immédiatement",
    "important", "critique", "alerte", "attention",
    "action requise", "réagissez", "réponse immédiate",
    "dernière chance", "maintenant", "tout de suite",
    "sans délai", "au plus vite", "asap"
]

financial_words = [
    "paiement", "payer", "facture", "montant", "somme",
    "remboursement", "rembourser", "transaction", "transfert",
    "virement", "compte", "bancaire", "banque", "carte",
    "crédit", "débit", "solde", "frais", "taxe", "impôt",
    "revenu", "argent", "financier", "finance"
]

threat_words = [
    "bloqué", "suspendu", "suspension", "désactivé",
    "fermé", "annulé", "risque", "danger", "sanction",
    "poursuite", "procédure", "amende", "punition",
    "obligatoire", "obligation", "infraction", "fraude",
    "violation", "non conforme", "non-conformité"
]

authority_words = [
    "gouvernement", "police", "gendarmerie", "tribunal",
    "justice", "administration", "impôts", "banque",
    "sécurité sociale", "assurance maladie", "caf",
    "edf", "orange", "free", "sfr",
    "service client", "support", "assistance",
    "autorité", "officiel", "ministère"
]

reward_words = [
    "gagner", "gagnant", "gagné", "gain",
    "cadeau", "récompense", "bonus", "prime",
    "offre", "promotion", "promo", "réduction",
    "gratuit", "gratuité", "remise", "coupon",
    "jackpot", "lot", "tirage", "concours"
]

greeting_words = [
    "bonjour", "bonsoir", "salut", "coucou",
    "bienvenue", "hello", "hi", "yo",
    "bonne journée", "bonne soirée",
    "cher", "chère", "chers", "chères",
    "madame", "monsieur", "mme", "mr", "m\\.", "mlle"
]

politeness_words = [
    "merci", "merci beaucoup", "je vous remercie",
    "s'il vous plaît", "svp", "stp",
    "cordialement", "bien cordialement",
    "sincèrement", "respectueusement",
    "avec mes salutations", "avec mes remerciements",
    "je reste à votre disposition",
    "je vous prie d'agréer",
    "toutes mes salutations"
]

signature_words = [
    "cordialement", "bien cordialement",
    "sincèrement", "respectueusement",
    "salutations distinguées", "salutations",
    "bien à vous", "amicalement",
    "merci d'avance", "merci encore",
    "votre dévoué", "votre serviteur",
    "meilleures salutations"
]


class NLP_Feat_Eng:
    def __init__(self, df, corpus_path=""):
        self.df = df
        self.corpus_path = corpus_path

        self.urgency_words = urgency_words
        self.financial_words = financial_words
        self.threat_words = threat_words
        self.authority_words = authority_words
        self.reward_words = reward_words

        self.greeting_words = greeting_words
        self.politeness_words = politeness_words
        self.signature_words = signature_words

        self.regex_decl = r'.*\.'
        self.regex_interrog = r".*\?"
        self.regex_elliptical = r".*\.{2,}"
        self.regex_exclam = r".*!{2,}"
        self.regex_emphatic_question = r"\?{2,}"
        self.regex_comma = r".*,"
        self.regex_upper_count = r"[A-ZÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸ]"
        self.regex_lower_count = r"[a-zàâäçéèêëîïôöùûüÿ]"
        self.regex_digit = r"\d"
        self.regex_word_digit = r"\b(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|quarante|cinquante|soixante|cent)\b"
        self.regex_money_digits = r"\b\d[\d.,]*\s?(€|\$|£)\b"
        self.regex_money_words = r"\b(un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|quarante|cinquante|soixante|cent)\s+(euros?|dollars?)\b"
        self.regex_phone = r"\b(\+33\s?[1-9](?:[\s.-]?\d{2}){4}|0[1-9](?:[\s.-]?\d{2}){4})\b"
        self.regex_email = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        self.regex_company_email = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.(fr|com|net|org|eu)\b"
        self.regex_contact = r"\bcontact@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        self.regex_support = r"\b(support|help|assistance)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        self.regex_noreply = r"\b(no-?reply)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
        self.regex_suspect_email = r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(xyz|win|ru|cn|top|biz)\b"
        self.emoji_pattern = (
            "["
                "\U0001F600-\U0001F64F"
                "\U0001F300-\U0001F5FF"
                "\U0001F680-\U0001F6FF"
                "\U0001F1E0-\U0001F1FF"
                "\u2700-\u27BF"
                "\U0001F900-\U0001F9FF"
                "\U0001FA70-\U0001FAFF"
                "]"
            )
        self.regex_urgency = r"\b(" + "|".join(urgency_words) + r")\b"
        self.regex_financial = r"\b(" + "|".join(financial_words) + r")\b"
        self.regex_threat = r"\b(" + "|".join(threat_words) + r")\b"
        self.regex_authority = r"\b(" + "|".join(authority_words) + r")\b"
        self.regex_reward = r"\b(" + "|".join(reward_words) + r")\b"
        self.regex_url = (
            r"(?:https?://[^\s]+|"      # http:// ou https://
            r"http//[^\s]+|"            # http// (sans :)
            r"http[#_/]//[^\s]+|"       # http#// ou http_//
            r"hxxp://[^\s]+|"           # hxxp://
            r"www\.[^\s]+)"             # www.
        )
        self.suspicious_tlds = [
            "xyz","top","win","bid","loan","click","info",
            "ru","cn","tk","ml","ga","cf","gq","work",
            "zip","mov","cam","rest","kim","party"
        ]

        self.regex_suspicious_url = (
            r"(?:https?://|http//|http[#_/]//|hxxp://|www\.)"
            r"[^\s]+\.(?:" + "|".join(self.suspicious_tlds) + r")\b"
        )
        self.shorteners = [
            r"bit\.ly", r"tinyurl\.com", r"t\.co", r"goo\.gl", r"ow\.ly",
            r"is\.gd", r"buff\.ly", r"rebrand\.ly", r"cutt\.ly", r"shorte\.st"
        ]

        self.regex_shortened = (
            r"(?:https?://|http//|http[#_/]//|hxxp://|www\.)?"
            r"(?:" + "|".join(self.shorteners) + r")/[^\s]+"
        )

        # Groupe 1 : je / j'
        self.pronouns_je = [r"je\b", r"j'"]
        # Groupe 2 : tu
        self.pronouns_tu = [r"tu\b"]
        # Groupe 3 : il / elle
        self.pronouns_il_elle = [r"il\b", r"elle\b"]
        # Groupe 4 : nous
        self.pronouns_nous = [r"nous\b"]
        # Groupe 5 : vous
        self.pronouns_vous = [r"vous\b"]
        # Groupe 6 : ils / elles
        self.pronouns_ils_elles = [r"ils\b", r"elles\b"]
        # Groupe 7 : on
        self.pronouns_on = [r"on\b"]
        self.regex_je = r"(" + "|".join(self.pronouns_je) + r")"
        self.regex_tu = r"(" + "|".join(self.pronouns_tu) + r")"
        self.regex_il_elle = r"(" + "|".join(self.pronouns_il_elle) + r")"
        self.regex_nous = r"(" + "|".join(self.pronouns_nous) + r")"
        self.regex_vous = r"(" + "|".join(self.pronouns_vous) + r")"
        self.regex_ils_elles = r"(" + "|".join(self.pronouns_ils_elles) + r")"
        self.regex_on = r"(" + "|".join(self.pronouns_on) + r")"
        self.regex_greeting = r"\b(" + "|".join(self.greeting_words) + r")\b"
        self.regex_politeness = r"\b(" + "|".join(self.politeness_words) + r")\b"
        self.regex_signature = r"\b(" + "|".join(self.signature_words) + r")\b"

        self.corpus_path = self.corpus_path

    @monitor.calculate_func_time
    def feature_engineering_full_pipeline(self, update_corpus=True):
        logging.info("Début du pipeline de feature engineering NLP")

        self.df["text"] = self.df["text"].fillna("").astype(str)

        self.message_length()
        self.word_count()
        self.count_declarative_caracters()
        self.count_interrogative_caracters()
        self.count_elliptical_caracters()
        self.count_emphatic_exclamations()
        self.count_emphatic_questions()
        self.count_commas()
        self.average_word_length()
        self.median_word_length()
        self.uppercase_count()
        self.lowercase_count()
        self.uppercase_ratio()
        self.digit_count()
        self.word_digit_count()
        self.money_count()
        self.money_words_count()
        self.phone_number_count()
        self.email_count()
        self.company_email_count()
        self.contact_email_count()
        self.support_email_count()
        self.noreply_email_count()
        self.suspect_email_count()
        self.special_character_count()
        self.line_break_count()
        self.tab_count()
        self.emoji_count()
        self.whitespace_count()
        self.special_character_ratio()

        self.lower_the_text()

        self.count_psycho_ugency_words()
        self.count_financial_words()
        self.count_threat_words()
        self.count_authority_words()
        self.count_reward_words()
        self.count_urls()
        self.count_suspicious_urls()
        self.count_shortened_urls()
        self.count_personal_pronouns()
        self.count_greetings()
        self.count_politeness()
        self.count_signatures()

        self.df["text_transformed"] = self.df["text_lower"]

        self.replace_money_info()
        self.replace_phone_info()
        self.replace_email_info()
        self.replace_psycho_urgency_words()
        self.replace_urls()
        self.replace_greetings_politeness_signatures()
        self.replace_digits()
        self.clean_special_characters()

        logging.info("Fin du pipeline de feature engineering NLP")

        if update_corpus:
            logging.info("Mise à jour ou création du corpus de mots connu")
            self.update_corpus(self.corpus_path)

        return self.df

    @monitor.calculate_func_time
    def message_length(self):
        """Cette méthode calcule la longueur de chaque message et 
        stocke le résultat dans une nouvelle colonne 'msg_length' du DataFrame.
        """
        self.df['msg_length'] = self.df['text'].str.len()
        

    @monitor.calculate_func_time
    def word_count(self):
        self.df["msg_word_count"] = self.df["text"].str.split().str.len()

    @monitor.calculate_func_time
    def count_declarative_caracters(self):
        """Cette méthode compte le nombre de phrases déclaratives dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'msg_declarative_sentence_count' du DataFrame.
        """
        self.df['msg_declarative_sentence_count'] = self.df['text'].str.count(self.regex_decl)

    @monitor.calculate_func_time
    def count_interrogative_caracters(self):
        """Cette méthode compte le nombre de phrases interrogatives dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'msg_interrogative_sentence_count' du DataFrame.
        """
        self.df['msg_interrogative_sentence_count'] = self.df['text'].str.count(self.regex_interrog)


    @monitor.calculate_func_time
    def count_elliptical_caracters(self):
        """Cette méthode compte le nombre de phrases eliptiques dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'msg_elliptical_sentence_count' du DataFrame.
        """
        self.df['msg_elliptical_sentence_count'] = self.df['text'].str.count(self.regex_elliptical)

    @monitor.calculate_func_time
    def count_emphatic_exclamations(self):
        """Cette méthode compte le nombre de phrases d'exclamation emphatiques dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'msg_emphatic_exclamation_sentence_count' du DataFrame.
        """
        self.df['msg_emphatic_exclamation_sentence_count'] = self.df['text'].str.count(self.regex_exclam)

    @monitor.calculate_func_time
    def count_emphatic_questions(self):
        """Cette méthode compte le nombre de phrases d'intérogation emphatiques dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'msg_emphatic_question_sentence_count' du DataFrame.
        """
        self.df['msg_emphatic_question_sentence_count'] = self.df['text'].str.count(self.regex_emphatic_question)

    @monitor.calculate_func_time
    def count_commas(self):
        """Cette méthode compte le nombre de virgules dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'coma_count' du DataFrame.
        """
        self.df['coma_count'] = self.df['text'].str.count(self.regex_comma  )

    @monitor.calculate_func_time
    def average_word_length(self):
        words = self.df["text"].str.findall(r"\b\w+\b")
        self.df["average_word_length"] = words.apply(
            lambda x: sum(map(len, x)) / len(x) if x else 0
        )

    @monitor.calculate_func_time
    def median_word_length(self):
        words = self.df["text"].str.findall(r"\b\w+\b")
        self.df["median_word_length"] = words.apply(
            lambda x: float(np.median([len(w) for w in x])) if x else 0
        )

    @monitor.calculate_func_time
    def uppercase_count(self):
        """Cette méthode compte le nombre de lettres majuscules dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'uppercase_count' du DataFrame.
        """
        self.df['uppercase_count'] = self.df['text'].str.count(self.regex_upper_count)

    @monitor.calculate_func_time
    def lowercase_count(self):
        """Cette méthode compte le nombre de lettres minuscules dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'lowercase_count' du DataFrame.
        """
        self.df['lowercase_count'] = self.df['text'].str.count(self.regex_lower_count)


    @monitor.calculate_func_time
    def uppercase_ratio(self):
        total_letters = self.df["uppercase_count"] + self.df["lowercase_count"]
        self.df["uppercase_ratio"] = np.where(
            total_letters > 0,
            self.df["uppercase_count"] / total_letters * 100,
            0
        )


    @monitor.calculate_func_time
    def digit_count(self):
        """Cette méthode compte le nombre de chiffres dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'digit_count' du DataFrame.
        """
        self.df['digit_count'] = self.df['text'].str.count(self.regex_digit)
        

    @monitor.calculate_func_time
    def word_digit_count(self):       
        """Cette méthode compte le nombre de mots représentant des chiffres dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'word_digit_count' du DataFrame.
        """
        self.df['word_digit_count'] = self.df['text'].str.count(self.regex_word_digit)


    @monitor.calculate_func_time
    def money_count(self):
        """Cette méthode compte le nombre de mentions d'argent dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'money_count' du DataFrame.
        """
        self.df["money_count"] = self.df["text"].str.count(self.regex_money_digits)


    @monitor.calculate_func_time
    def money_words_count(self):
        """Cette méthode compte le nombre de mentions d'argent écrites en toutes lettres dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'money_words_count' du DataFrame.
        """
        self.df["money_words_count"] = self.df["text"].str.count(self.regex_money_words)


    @monitor.calculate_func_time
    def phone_number_count(self):
        """Cette méthode compte le nombre de numéros de téléphone dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'phone_number_count' du DataFrame.
        """
        self.df["phone_number_count"] = self.df["text"].str.count(self.regex_phone)

    @monitor.calculate_func_time
    def email_count(self):        
        """Cette méthode compte le nombre d'adresses e-mail dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'email_count' du DataFrame.
        """
        self.df["email_count"] = self.df["text"].str.count(self.regex_email)

    @monitor.calculate_func_time
    def company_email_count(self):        
        """Cette méthode compte le nombre d'adresses e-mail d'entreprise dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'company_email_count' du DataFrame.
        """
        self.df["company_email_count"] = self.df["text"].str.count(self.regex_company_email)


    @monitor.calculate_func_time
    def contact_email_count(self):
        """Cette méthode compte le nombre d'adresses e-mail de contact dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'contact_email_count' du DataFrame.
        """
        self.df["contact_email_count"] = self.df["text"].str.count(self.regex_contact)


    @monitor.calculate_func_time
    def support_email_count(self):
        """Cette méthode compte le nombre d'adresses e-mail de support dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'support_email_count' du DataFrame.
        """
        self.df["support_email_count"] = self.df["text"].str.count(self.regex_support)


    @monitor.calculate_func_time
    def noreply_email_count(self):
        """Cette méthode compte le nombre d'adresses e-mail de type 'no-reply' dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'noreply_email_count' du DataFrame.
        """
        self.df["noreply_email_count"] = self.df["text"].str.count(self.regex_noreply)


    @monitor.calculate_func_time
    def suspect_email_count(self):
        """Cette méthode compte le nombre d'adresses e-mail suspectes dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'suspect_email_count' du DataFrame.
        """
        self.df["suspect_email_count"] = self.df["text"].str.count(self.regex_suspect_email)
        

    @monitor.calculate_func_time
    def special_character_count(self):
        """Cette méthode compte le nombre de caractères spéciaux dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'special_character_count' du DataFrame.
        """
        self.df["special_character_count"] = self.df["text"].str.count(r"[^a-zA-Z0-9\s]")


    @monitor.calculate_func_time
    def line_break_count(self):
        """Cette méthode compte le nombre de sauts de ligne dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'line_break_count' du DataFrame.
        """
        self.df["line_break_count"] = self.df["text"].str.count(r"\n")


    @monitor.calculate_func_time
    def tab_count(self):
        """Cette méthode compte le nombre de tabulations dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'tab_count' du DataFrame.
        """
        self.df["tab_count"] = self.df["text"].str.count(r"\t")


    @monitor.calculate_func_time
    def emoji_count(self):
        """Cette méthode compte le nombre d'emojis dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'emoji_count' du DataFrame.
        """
        self.df["emoji_count"] = self.df["text"].str.count(self.emoji_pattern)


    @monitor.calculate_func_time
    def whitespace_count(self):
        """Cette méthode compte le nombre de caractères d'espacement dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'whitespace_count' du DataFrame.
        """
        self.df["whitespace_count"] = self.df["text"].str.count(r"\s")


    @monitor.calculate_func_time
    def special_character_ratio(self):
        self.df["special_character_ratio"] = np.where(
            self.df["msg_length"] > 0,
            self.df["special_character_count"] / self.df["msg_length"] * 100,
            0
        )

    @monitor.calculate_func_time
    def lower_the_text(self):
        """Cette méthode convertit le texte de chaque message en minuscules 
        et stocke le résultat dans une nouvelle colonne 'text_lower' du DataFrame.
        """
        self.df["text_lower"] = self.df["text"].str.lower()


    @monitor.calculate_func_time
    def count_psycho_ugency_words(self):
        """Cette méthode compte le nombre de mots d'urgence psychologique dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'urgency_word_count' du DataFrame.
        """
        self.df["urgency_word_count"] = self.df["text_lower"].str.count(self.regex_urgency)


    @monitor.calculate_func_time
    def count_financial_words(self):
        """Cette méthode compte le nombre de mots financiers dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'financial_word_count' du DataFrame.
        """
        self.df["financial_word_count"] = self.df["text_lower"].str.count(self.regex_financial)


    @monitor.calculate_func_time
    def count_threat_words(self):
        """Cette méthode compte le nombre de mots de menace dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'threat_word_count' du DataFrame.
        """
        self.df["threat_word_count"] = self.df["text_lower"].str.count(self.regex_threat)


    @monitor.calculate_func_time
    def count_authority_words(self):
        """Cette méthode compte le nombre de mots d'autorité dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'authority_word_count' du DataFrame.
        """
        self.df["authority_word_count"] = self.df["text_lower"].str.count(self.regex_authority)


    @monitor.calculate_func_time
    def count_reward_words(self):
        """Cette méthode compte le nombre de mots de récompense dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'reward_word_count' du DataFrame.
        """
        self.df["reward_word_count"] = self.df["text_lower"].str.count(self.regex_reward)


    @monitor.calculate_func_time
    def count_urls(self):
        """Cette méthode compte le nombre d'URLs dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'url_count' du DataFrame.
        """
        self.df["url_count"] = self.df["text_lower"].str.count(self.regex_url)


    @monitor.calculate_func_time
    def count_suspicious_urls(self):
        """Cette méthode compte le nombre d'URLs suspectes dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'suspicious_url_count' du DataFrame.
        """
        self.df["suspicious_url_count"] = self.df["text_lower"].str.count(self.regex_suspicious_url)


    @monitor.calculate_func_time
    def count_shortened_urls(self):
        """Cette méthode compte le nombre d'URLs raccourcies dans chaque message 
        en utilisant une expression régulière et stocke le résultat dans une nouvelle 
        colonne 'shortened_url_count' du DataFrame.
        """
        self.df["shortened_url_count"] = self.df["text_lower"].str.count(self.regex_shortened)


    @monitor.calculate_func_time
    def count_personal_pronouns(self):
        """Cette méthode compte le nombre de pronoms personnels dans chaque message 
        en utilisant des expressions régulières pour chaque groupe de pronoms et stocke 
        les résultats dans de nouvelles colonnes du DataFrame.
        """
        self.df["je_count"] = self.df["text_lower"].str.count(self.regex_je)
        self.df["tu_count"] = self.df["text_lower"].str.count(self.regex_tu)
        self.df["il_elle_count"] = self.df["text_lower"].str.count(self.regex_il_elle)
        self.df["nous_count"] = self.df["text_lower"].str.count(self.regex_nous)
        self.df["vous_count"] = self.df["text_lower"].str.count(self.regex_vous)
        self.df["ils_elles_count"] = self.df["text_lower"].str.count(self.regex_ils_elles)
        self.df["on_count"] = self.df["text_lower"].str.count(self.regex_on)
        

    @monitor.calculate_func_time
    def count_greetings(self):
        """Cette méthode compte le nombre de mots de salutation dans chaque message
        en utilisant une expression régulière et stocke le résultat dans une nouvelle
        colonne 'has_greeting' du DataFrame.
        """
        self.df["has_greeting"] = self.df["text_lower"].str.contains(self.regex_greeting, regex=True).astype(int)


    @monitor.calculate_func_time
    def count_politeness(self):
        """Cette méthode compte le nombre de mots de politesse dans chaque message
        en utilisant une expression régulière et stocke le résultat dans une nouvelle
        colonne 'has_politeness' du DataFrame.
        """
        self.df["has_politeness"] = self.df["text_lower"].str.contains(self.regex_politeness, regex=True).astype(int)

    @monitor.calculate_func_time
    def count_signatures(self):
        """Cette méthode compte le nombre de mots de signature dans chaque message
        en utilisant une expression régulière et stocke le résultat dans une nouvelle
        colonne 'has_signature' du DataFrame.
        """
        self.df["has_signature"] = self.df["text_lower"].str.contains(self.regex_signature, regex=True).astype(int)


    @monitor.calculate_func_time
    def replace_money_info(self):
        self.df["text_transformed"] = (
            self.df["text_transformed"]
            .str.replace(self.regex_money_digits, "[MONEY]", regex=True)
            .str.replace(self.regex_money_words, "[MONEY]", regex=True)
        )


    @monitor.calculate_func_time
    def replace_phone_info(self):
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(
            self.regex_phone,
            "[PHONE]",
            regex=True
        )


    @monitor.calculate_func_time
    def replace_email_info(self):
        """Cette méthode remplace les adresses e-mail dans le texte de chaque message
        par des tokens génériques en utilisant des expressions régulières pour différents types d'e-mails.
        """
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_company_email, "[CORP_EMAIL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_contact, "[CONTACT_EMAIL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_noreply, "[NO_REPLY_EMAIL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_suspect_email, "[SUSPECT_EMAIL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_email, "[EMAIL]", regex=True)


    @monitor.calculate_func_time
    def replace_psycho_urgency_words(self):
        """Cette méthode remplace les mots d'urgence psychologique dans le texte de chaque message
        par un token générique '[URGENCY]' en utilisant une expression régulière.
        """
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_urgency, "[URGENCY]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_financial, "[FINANCIAL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_threat, "[THREAT]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_authority, "[AUTHORITY]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_reward, "[REWARD]", regex=True)


    @monitor.calculate_func_time
    def replace_urls(self):
        """Cette méthode remplace les URLs dans le texte de chaque message
        par des tokens génériques en utilisant des expressions régulières pour différents types d'URLs.
        """
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_suspicious_url, "[SUSPICIOUS_URL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_shortened, "[SHORTENED_URL]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_url, "[URL]", regex=True)


    @monitor.calculate_func_time
    def replace_greetings_politeness_signatures(self):
        """Cette méthode remplace les mots de salutation, de politesse et de 
        signature dans le texte de chaque message
        par des tokens génériques en utilisant des expressions 
        régulières pour chaque catégorie de mots.
        """
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_greeting, "[GREETING]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_politeness, "[POLITENESS]", regex=True)
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_signature, "[SIGNATURE]", regex=True)


    @monitor.calculate_func_time
    def replace_digits(self):
        """Cette méthode remplace les chiffres et les mots représentant des 
        chiffres dans le texte de chaque message
        par des tokens génériques en utilisant des expressions régulières.
        """
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_digit, "[DIGIT]", regex=True) 
        self.df["text_transformed"] = self.df["text_transformed"].str.replace(self.regex_word_digit, "[W_DIGIT]", regex=True) 


    @monitor.calculate_func_time   
    def remove_special_chars(self, text):
        """Cette méthode supprime les caractères spéciaux du texte de chaque message
        en utilisant des expressions régulières pour remplacer les caractères indésirables par des espaces.
        """
        # remplacer apostrophes et tirets par espace
        text = re.sub(r"[-']", " ", text)

        # supprimer autres caractères spéciaux
        text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s\[\]]", " ", text)

        # retirer espaces multiples
        text = re.sub(r"\s+", " ", text).strip()

        return text


    @monitor.calculate_func_time 
    def clean_special_characters(self):
        self.df["text_final"] = (
            self.df["text_transformed"]
            .str.replace(r"[-']", " ", regex=True)
            .str.replace(r"[^a-zA-ZÀ-ÿ0-9\s\[\]]", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
    

    @monitor.calculate_func_time
    def update_corpus(self, corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)

        new_tokens = (
            self.df["text_final"]
            .dropna()
            .str.split()
            .explode()
            .dropna()
            .drop_duplicates()
            .to_frame("token")
            .reset_index(drop=True)
        )

        if os.path.exists(corpus_path):
            old_tokens = pd.read_parquet(corpus_path)
            df_corpus = pd.concat([old_tokens, new_tokens], ignore_index=True)
            df_corpus = df_corpus.drop_duplicates(subset=["token"], keep="first")
        else:
            df_corpus = new_tokens

        df_corpus.to_parquet(corpus_path, index=False)
        