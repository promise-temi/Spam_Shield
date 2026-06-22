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
