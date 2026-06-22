from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()
import logging

class Security:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(self.key.encode())

    def encrypt_(self, value:str)->str:
        """ 
        Permet de chiffrer les données sensibles avec fernet, (robuste, simple et propre)
        """
        if value is None:
            return None
        try:
            return self.fernet.encrypt(value.encode("utf-8")).decode("utf-8")
        except Exception as err:
            logging.error(f"Une erreur s'est produite pendant l'encryptage: {err}")

    def decrypt_(self, token:str)->str:
        """ 
        Permet de dechiffrer les données sensibles chiffré avec fernet, (robuste, simple et propre)
        """
        if token is None:
            return None
        try:
            return self.fernet.decrypt(token.encode("utf-8")).decode("utf-8")
        except Exception as err:
            logging.error(f"Une erreur s'est produite pendant l'encryptage: {err}")


