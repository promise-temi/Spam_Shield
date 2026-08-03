from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
load_dotenv()
import logging

class Security:
    def __init__(self):
        self.key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(self.key.encode())
        self.API_KEY = os.getenv("BACKEND_API_KEY")
        if not self.API_KEY:
            raise RuntimeError("La variable d'environnement BACKEND_API_KEY est absente.")

    def verify_api_key(self, x_api_key: str) -> bool:
        """Vérifie que la clé API transmise correspond à la clé attendue."""
        return x_api_key == self.API_KEY
    
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

    def anonymize_metadata(self, metadata_: dict) -> dict:

        metadata = metadata_.copy()

        if "email" in metadata and metadata["email"]:
            try:
                email = metadata["email"]
                login, domain = email.split("@")
                metadata["email"] = login[:2] + "****@" + domain
            except ValueError:
                return metadata_["email"]


        if "phone" in metadata and metadata["phone"]:
            try:
                phone = metadata["phone"]
                metadata["phone"] = phone[:2] + "*" * (len(phone) - 2)
            except ValueError:
                            return metadata_["phone"]

        if "name" in metadata and metadata["name"]:
            try:
                name = metadata["name"]
                metadata["name"] = name[0] + "*" * (len(name) - 1)
            except ValueError:
                return metadata_["name"]

        if "surname" in metadata and metadata["surname"]:
            try:
                surname = metadata["surname"]
                metadata["surname"] = surname[0] + "*" * (len(surname) - 1)
            except ValueError:
                return metadata_["surname"]

        return metadata

