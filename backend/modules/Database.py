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
    def __init__(self, sql_file_path=f"{os.path.dirname(__file__)}/data/db.sql"):
        self.sql_file_path = sql_file_path
        self._connect()
        self._create_tables_if_not_exist()
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
            raise e


    def _create_tables_if_not_exist(self):
        try:
            with open(self.sql_file_path, "r") as f:
                sql_script = f.read()
            cur = self.conn.cursor()
            cur.execute(sql_script)
            self.conn.commit()
            cur.close()
            logging.info("Tables crées avec succès ou déja existantes")
        except FileNotFoundError as e:
            logging.error(f"Une erreur s'est produite lors de la création des tables dans la BDD : \n {e}")
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
        self.conn.commit()
        cur.close()

    def get_prospect_mail(self, query="*")-> list:
       cur = self.conn.cursor()
       try:
        cur.execute(f"SELECT email FROM Prospects_mails")
        rows = cur.fetchall()
        logging.debug(rows)
        decrypted_prospect_mails = [self.security_tools.decrypt_(row[0]) for row in rows]
        return [mail for mail in decrypted_prospect_mails]
       except Exception as e:
                logging.error(f"Une erreur s'est produite pendant la reccupération des mails : {e}")

    def get_prospect_mail_front(self, query="*") -> list:
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id, email FROM Prospects_mails")
            rows = cur.fetchall()
            decrypted = [
                {"id": row[0], "email": self.security_tools.decrypt_(row[1])}
                for row in rows
            ]
            return decrypted
        except Exception as e:
            logging.error(f"Erreur récupération mails : {e}")

    def check_if_mail_exist(self, new_mail):
        old_mails = self.get_prospect_mail('email')
        for old_mail in old_mails:
            if new_mail == old_mail:
                logging.info('Ce mail existe déjà dans la base')
                return True
            
        logging.info('Nouveau mail détecté')
        return False
    


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

    def save_message(self, pred_text, raw_text, metadata, banned_patterns_found, model_pred, model_confidence, business_rules_label, final_label, is_overridden):
        cur = self.conn.cursor()
        cur.execute(f"""INSERT INTO messages 
                    (preprocessed_text, 
                    crypted_text, 
                    metadata, 
                    model_label, 
                    model_confidence,
                    business_rules_label, 
                    final_label,
                    banned_patterns_found,
                    is_overridden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                    (pred_text,
                     self.security_tools.encrypt_(raw_text), 
                     self.security_tools.encrypt_(json.dumps(metadata)), 
                     model_pred, 
                     model_confidence,
                     business_rules_label, 
                     final_label,
                     banned_patterns_found,
                     is_overridden,))
        self.conn.commit()
        cur.close()
        logging.info("Message enregistré avec succès dans la bdd")

    
    def set_new_phase(self, start, end):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO periods (start_date, end_date) VALUES (%s, %s)", (start, end,))
        self.conn.commit()
        cur.close()
        logging.info(f"phase enregistré avec succès dans la bdd")
    
    def get_current_phase(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM periods ORDER BY start_date DESC LIMIT 1")
        row = cur.fetchone()    
        return row

    def get_total_messages(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM messages")
        total_messages = cur.fetchone()[0]
        return total_messages
    
    def get_total_spam(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM messages WHERE final_label = TRUE")
        total_spam = cur.fetchone()[0]
        return total_spam
    
    def get_total_ham(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM messages WHERE final_label = FALSE")
        total_ham = cur.fetchone()[0]
        return total_ham
    
    def get_total_spam_rules(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM messages WHERE business_rules_label = TRUE")
        total_spam_rules = cur.fetchone()[0]
        return total_spam_rules
    
    def get_mean_confidence_score(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT AVG(model_confidence) FROM messages WHERE model_confidence IS NOT NULL")
        mean_confidence_score = cur.fetchone()[0]
        return mean_confidence_score
    
    def get_mean_confidence_score_spam(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT AVG(model_confidence) FROM messages WHERE model_confidence IS NOT NULL AND final_label = TRUE")
        mean_confidence_score_spam = cur.fetchone()[0]
        return mean_confidence_score_spam
    
    def get_mean_confidence_score_ham(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT AVG(model_confidence) FROM messages WHERE model_confidence IS NOT NULL AND final_label = FALSE")
        mean_confidence_score_ham = cur.fetchone()[0]
        return mean_confidence_score_ham
    
    def get_banned_patterns_found_count(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT COUNT(*)
            FROM messages
            WHERE banned_patterns_found IS NOT NULL
            AND cardinality(banned_patterns_found) > 0
        """)
        banned_patterns_found_count = cur.fetchone()[0]
        cur.close()
        return banned_patterns_found_count
    
    def get_all_anonymized_messages(self):
        cur = self.conn.cursor()
        cur.execute("SELECT preprocessed_text, model_label from messages")
        rows = cur.fetchall()
        messages = []
        for row in rows:
            message = {
                "text": row[0],
                "label": row[1]
            }
            messages.append(message)
        return messages

    def delete_all_messages(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM messages")
        self.conn.commit()
        cur.close()
        logging.info("Tous les messages ont été supprimés de la base de données")

    def get_all_regex_rules(self):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT id, pattern FROM regexes")
        except Exception as e:
            print("ERREUR SQL :", e)
            self.conn.rollback()
        rows = cur.fetchall()
        regex_rules = []
        for row in rows:
            rule = {
                "id": row[0],
                "pattern": row[1]
            }
            regex_rules.append(rule)
        return regex_rules
    
    def add_regex_rule(self, pattern:str):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO regexes (pattern) VALUES (%s);", (pattern,))
        except Exception as e:
            print("ERREUR SQL :", e)
            self.conn.rollback()
        self.conn.commit()
        cur.close()
        logging.info(f"La règle regex '{pattern}' a été ajoutée à la base de données.")


    def delete_regex_rule(self, id:int):
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM regexes WHERE id = (%s);", (id,))
        except Exception as e:
            print("ERREUR SQL :", e)
            self.conn.rollback()
        self.conn.commit()
        cur.close()
        logging.info(f"La règle regex avec l'ID '{id}' a été supprimée de la base de données.")

    def update_message_label(self, id:int):
        cur = self.conn.cursor()
        # modifier if edited a l'opposé de ce qu'il est actuellement
        cur.execute("Update messages SET is_edited = NOT is_edited WHERE id = (%s);", (id,))
        cur.execute("UPDATE messages SET edition_counter = edition_counter + 1 WHERE id = (%s);", (id,))
        cur.execute("UPDATE messages SET final_label = NOT final_label WHERE id = (%s);", (id,))
        self.conn.commit()
        cur.close()
        logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")

    def get_all_messages(self):
        pass