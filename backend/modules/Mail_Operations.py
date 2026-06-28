import os
import logging
from dotenv import load_dotenv
load_dotenv()
import smtplib
from email.message import EmailMessage
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Database import Postgres_DB


class Mail_Operations:
    def __init__(self):
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.DB = Postgres_DB()
        self.prospects = self.DB.get_prospect_mail('email')
        print(self.prospects)


    def send_mail(self, message, metadata):
        logging.info('Début Envoi')
        for mail in self.prospects:
            logging.info('Envoie du message')
            msg = EmailMessage()
            msg["From"] = self.email_address
            msg["To"] = mail
            msg["Subject"] = f"SpamShield - Nouveau message {(' : ' + metadata['subject']) if metadata['subject'] else ''}"
            msg.set_content(f"""Nom : {metadata['surname'] if metadata['surname'] else '__'}\nPrenom : {metadata['name'] if metadata['name'] else '__'}\nEmail : {metadata['email'] if metadata['email'] else '__'}\nTelephone : {metadata['phone'] if metadata['phone'] else '__'}\n\n\n{str(message)}\n\n\n\n\nCe type de messages ne vous semble pas pertinant? Aidez Spamshield à mieux comprendre vos besoins. Consulter votre tableau de bord SpamShield pour ajuster vos préférences et affiner les prochaines analyses""")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            logging.info('Message envoyé avec succès')
        logging.info('Fin Envoi')


    def get_total_messages(self):
        total_messages = self.DB.get_total_messages()
        return total_messages
    
    def get_total_spam(self):
        total_spam = self.DB.get_total_spam()
        return total_spam
    
    def get_total_ham(self):
        total_ham = self.DB.get_total_ham()
        return total_ham
    
    def get_total_spam_rules(self):
        total_spam_rules = self.DB.get_total_spam_rules()
        return total_spam_rules
    
    def get_mean_confidence_score(self):
        mean_confidence_score = self.DB.get_mean_confidence_score()
        return mean_confidence_score
    def get_mean_confidence_score_spam(self):
        mean_confidence_score_spam = self.DB.get_mean_confidence_score_spam()
        return mean_confidence_score_spam
    
    def get_mean_confidence_score_ham(self):
        mean_confidence_score_ham = self.DB.get_mean_confidence_score_ham()
        return mean_confidence_score_ham
    
    def get_banned_patterns_found_count(self):
        banned_patterns_found_count = self.DB.get_banned_patterns_found_count()
        return banned_patterns_found_count
        

    def send_report(self, phase_start, phase_end, deadline):
        logging.info('Début Envoi')
        for mail in self.prospects:
            logging.info('Envoie du message')
            msg = EmailMessage()
            msg["From"] = self.email_address
            msg["To"] = mail
            msg["Subject"] = f"SpamShield - Nouveau Rapport"
            msg.set_content(f"""Rapport SpamShield du {phase_start} au {phase_end}\n
                            Messages Totaux : {self.get_total_messages() if self.get_total_messages() else '__'}
                            \nSpam : {self.get_total_spam() if self.get_total_spam() else '__'}
                            \nHam : {self.get_total_ham() if self.get_total_ham() else '__'}
                            \nSpam Règles Metier : {self.get_total_spam_rules() if self.get_total_spam_rules() else '__'}
                            \n\n\n\n\nA la reception de ce rapport, vous avez jusqu'au {deadline} pour apporter des corrections avant que les messages et données associées ne soient définitivement supprimées.
                            \n Aidez Spamshield à mieux comprendre vos besoins. Consulter votre tableau de bord SpamShield pour ajuster vos préférences et affiner les prochaines analyses""")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
            logging.info('Message envoyé avec succès')
        logging.info('Fin Envoi')
