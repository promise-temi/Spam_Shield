import psycopg2
import json
import os
from dotenv import load_dotenv
load_dotenv()
import logging
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Secure import Security



class Postgres_DB:
    def __init__(self, sql_file_path=""):
        self.sql_file_path = sql_file_path
        self._connect()
        self.security_tools = Security()

    def _connect(self):
        try :
            self.conn = psycopg2.connect(
                database = os.getenv("DB_DATABASE"), 
                user = os.getenv("DB_USER"), 
                host= os.getenv("DB_HOST"), 
                password = os.getenv("DB_PASSWORD"), 
                port = os.getenv("DB_PORT"))
            logging.info("Connexion à la base Postgres réussie")
        except Exception as e:
            logging.error(f"La connexion à la base Postgres à échouée : \n {e}")


    def create_tables_if_not_exist(self):
        try:
            with open(self.sql_file_path, "r") as f:
                sql_script = f.read()
            cur = self.conn.cursor()
            cur.execute(sql_script)
            self.conn.commit()
            cur.close()
            logging.info("Tables crées avec succès ou déja existantes")
        except Exception as e:
            logging.error(f"Une erreur s'est produite lors de la création des tables dans la BDD : \n {e}")

    def add_prospect_mail(self, mails:list[str]):
        cur = self.conn.cursor()
        for mail in mails:
            if self.check_if_mail_exist(mail):
                continue
            try:
                encrypted_mail = self.security_tools.encrypt_(mail)
                cur.execute("INSERT INTO Prospects_mails (email) VALUES (%s);", (encrypted_mail,))
                self.conn.commit()
                cur.close()
            except Exception as e:
                logging.error(f"Une erreur s'est produite pendant l'ajout d'un nouveau mail : {e}")

    def delete_prospect_mail(self, mails_ids:list[str]):
        cur = self.conn.cursor()
        for mail_id in mails_ids:
            try:
                cur.execute("DELETE FROM Prospects_mails WHERE id = (%s);", (mail_id,))
            except Exception as e:
                logging.error(f"Une erreur s'est produite pendant la supression mail : {e}")
            
    def get_prospect_mail(self, query)-> list:
       cur = self.conn.cursor()
       try:
        cur.execute(f"SELECT {query} FROM Prospects_mails")
        rows = cur.fetchall()
        logging.debug(rows)
        decrypted_prospect_mails = [self.security_tools.decrypt_(row[0]) for row in rows]
        return [mail for mail in decrypted_prospect_mails]
       except Exception as e:
                logging.error(f"Une erreur s'est produite pendant la reccupération des mails : {e}")

    def check_if_mail_exist(self, new_mail):
        old_mails = self.get_prospect_mail('email')
        for old_mail in old_mails:
            if new_mail == old_mail:
                logging.info('Ce mail existe déjà dans la base')
                return True
            
        logging.info('Nouveau mail détecté')
        return False
    
    def select_metadata_value(self, metadata_item_name):
        cur = self.conn.cursor()
        cur.execute("SELECT is_mandatory FROM metadata_options WHERE option_name = (%s);", (metadata_item_name,))
        data = cur.fetchone()
        logging.debug(data)
        return data

    def get_regexes_patterns(self):
        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT pattern FROM regexes;")
            rows = cur.fetchall()
            logging.debug(rows)
            regexes_list = [row[0] for row in rows]
            return [fr"{regex}" for regex in regexes_list]
        except Exception as e:
                    logging.error(f"Une erreur s'est produite pendant la reccupération des regexes : {e}")

    def save_message(self, pred_text, raw_text, metadata, banned_patterns_found, model_pred, business_rules_label, final_label):
        cur = self.conn.cursor()
        cur.execute(f"""INSERT INTO messages 
                    (preprocessed_text, 
                    crypted_text, 
                    metadata, 
                    model_label, 
                    business_rules_label, 
                    final_label,
                    banned_patterns_found) VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                    (pred_text,
                     self.security_tools.encrypt_(raw_text), 
                     self.security_tools.encrypt_(json.dumps(metadata)), 
                     model_pred, 
                     business_rules_label, 
                     final_label,
                     banned_patterns_found,))
        self.conn.commit()
        cur.close()
        logging.info("Message enregistré avec succès dans la bdd")

