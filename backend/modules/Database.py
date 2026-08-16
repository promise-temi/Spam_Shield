import psycopg2
import json
import os
from dotenv import load_dotenv
load_dotenv()
import logging
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from Secure import Security
import pandas as pd



class Postgres_DB:
    def __init__(self, sql_file_path=f"{os.path.dirname(__file__)}/data/db.sql", prod=True):
        self.sql_file_path = sql_file_path
        self.prod = prod
        self._connect()
        self._create_tables_if_not_exist()
        self.security_tools = Security()
        


    def _connect(self):

        if self.prod:
            database = os.getenv("DB_DATABASE")
            user = os.getenv("DB_USER")
            host = os.getenv("DB_HOST")
            password = os.getenv("DB_PASSWORD")
            port = os.getenv("DB_PORT")
        else:
            database = os.getenv("TEST_DB_DATABASE")
            user = os.getenv("TEST_DB_USER")
            host = os.getenv("TEST_DB_HOST")
            password = os.getenv("TEST_DB_PASSWORD")
            port = os.getenv("TEST_DB_PORT")

        try:
            self.conn = psycopg2.connect(
                database=database,
                user=user,
                host=host,
                password=password,
                port=port,
            )

            logging.info(
                f"Connexion {'TEST' if not self.prod else 'PROD'} réussie"
            )

        except Exception as e:
            logging.error(f"Connexion échouée : {e}")
            raise


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

    def select_message(self, id: int):
        cur = self.conn.cursor()
        try:
            cur.execute(
                """SELECT * FROM messages WHERE id = %s;""", (id,))
            row = cur.fetchone()
            
            selected_message = {
                "id": row[0],
                "message": self.security_tools.decrypt_(row[2]),
                "metadata": json.loads(self.security_tools.decrypt_(row[3])),
                "date": row[4].isoformat(),
                "model_label": row[5],
                "model_confidence": row[6],
                "business_rules_label": row[7],
                "final_label": row[8],
                "corrected": row[9],
                "overridden": row[10],
                "edition_counter": row[11],
                "banned_patterns_found": row[12],
                "period_id": row[13],
                "receaved": row[14],
                "consulted": row[15]
            }

            return selected_message

        except Exception as e:
            logging.error(
                f"Erreur récupération message {id}: {e}"
            )
            return None

        finally:
            cur.close()

    def get_all_messages(self, trier_par="date_desc", filtrer_par="*"):
        cur = self.conn.cursor()
        query = "SELECT * FROM messages"
        conditions = []

        # -------------------------
        # FILTRES
        # -------------------------
        if filtrer_par == "spam":
            conditions.append("final_label = TRUE")

        elif filtrer_par == "ham":
            conditions.append("final_label = FALSE")

        elif filtrer_par == "corriges":
            conditions.append("is_corected = TRUE")

        elif filtrer_par == "reclasses":
            conditions.append("is_overridden = TRUE")

        elif filtrer_par == "interdits":
            conditions.append("business_rules_label = TRUE")

        # Ajouter WHERE si nécessaire
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # -------------------------
        # TRI
        # -------------------------
        if trier_par == "date_desc":
            query += " ORDER BY created_at DESC"
        elif trier_par == "date_asc":
            query += " ORDER BY created_at ASC"

        # -------------------------
        # EXECUTION
        # -------------------------
        try:
            cur.execute(query)
            rows = cur.fetchall()
            selected_messages = [
                {
                    "id": row[0],
                    "metadata": self.security_tools.anonymize_metadata(
                        json.loads(self.security_tools.decrypt_(row[3]))
                    ),
                    "date": row[4].isoformat(),
                    "final_label": row[8]
                }
                for row in rows
            ]
            return selected_messages

        except Exception as e:
            logging.error(f"Erreur récupération messages : {e}")
            raise e



    
    def get_dashboard_metrics(self):

        cur = self.conn.cursor()

        try:

            metrics = {}

            # -------------------
            # KPIs globaux
            # -------------------

            cur.execute("SELECT COUNT(*) FROM messages")
            metrics["messages"] = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE final_label = FALSE
            """)
            metrics["legitimes"] = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE final_label = TRUE
            """)
            metrics["indesirables"] = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE is_corected = TRUE
            """)
            metrics["corrections"] = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE is_overridden = TRUE
            """)
            metrics["reclassements"] = cur.fetchone()[0]

            # -------------------
            # Distribution
            # -------------------

            distribution = {}

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE model_label = FALSE
            """)

            distribution["ham_prediction_ia"] = cur.fetchone()[0]
            metrics["ham_prediction_ia"] = distribution["ham_prediction_ia"]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE model_label = TRUE
            """)
            distribution["spam_prediction_ia"] = cur.fetchone()[0]
            metrics["spam_prediction_ia"] = distribution["spam_prediction_ia"]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE business_rules_label = TRUE
            """)
            distribution["spam_patterns_interdits"] = cur.fetchone()[0]
            metrics["spam_patterns_interdits"] = distribution["spam_patterns_interdits"]

            
            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE is_overridden = TRUE
            """)
            distribution["spam_override"] = cur.fetchone()[0]
            metrics["spam_override"] = distribution["spam_override"]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE is_corected = TRUE
                AND final_label = FALSE
            """)
            distribution["ham_corriges"] = cur.fetchone()[0]
            metrics["ham_corriges"] = distribution["ham_corriges"]

            cur.execute("""
                SELECT COUNT(*)
                FROM messages
                WHERE is_corected = TRUE
                AND final_label = TRUE
            """)
            distribution["spam_corriges"] = cur.fetchone()[0]
            metrics["spam_corriges"] = distribution["spam_corriges"]
            # -------------------
            # Métriques IA
            # -------------------

            cur.execute("""
                SELECT AVG(model_confidence)
                FROM messages
            """)
            metrics["avg_confidence"] = float(
                cur.fetchone()[0] or 0
            )

            cur.execute("""
                SELECT AVG(model_confidence)
                FROM messages
                WHERE final_label = TRUE
            """)
            metrics["avg_confidence_spam"] = float(
                cur.fetchone()[0] or 0
            )

            cur.execute("""
                SELECT AVG(model_confidence)
                FROM messages
                WHERE final_label = FALSE
            """)
            metrics["avg_confidence_ham"] = float(
                cur.fetchone()[0] or 0
            )

            cur.execute("""
                SELECT AVG(
                    COALESCE(
                        array_length(
                            banned_patterns_found,
                            1
                        ),
                        0
                    )
                )
                FROM messages
            """)
            metrics["avg_banned_patterns"] = float(
                cur.fetchone()[0] or 0
            )

            metrics["correction_rate"] = (
                metrics["corrections"]
                / metrics["messages"]
            )

            metrics["override_rate"] = (
                metrics["reclassements"]
                / metrics["messages"]
            )

            metrics["ham_corriges"] = distribution["ham_corriges"]
            metrics["spam_corriges"] = distribution["spam_corriges"]
        

            final_data = {
                "metrics": metrics,
                "distribution_par_categorie": distribution
            }
            final_data["distribution_par_categorie"]['graph_list'] = [final_data["distribution_par_categorie"]["ham_prediction_ia"],final_data["distribution_par_categorie"]["spam_prediction_ia"],final_data["distribution_par_categorie"]["spam_patterns_interdits"],final_data["distribution_par_categorie"]["spam_override"],final_data["distribution_par_categorie"]["ham_corriges"],final_data["distribution_par_categorie"]["spam_corriges"]]
            
            return final_data

        except Exception as e:
            logging.error(
                f"Erreur récupération dashboard : {e}"
            )
            return None

        finally:
            cur.close()

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
        cur.execute(
            """
            UPDATE messages
            SET
                is_corected = NOT is_corected,
                final_label = NOT final_label,
                edition_counter = edition_counter + 1
            WHERE id = %s;
            """,
            (id,)
        )        
        self.conn.commit()
        cur.close()
        logging.info(f"Le label du message avec l'ID '{id}' a été mis à jour avec succès.")





    def save_anonimized_messages(self, before, parquet_path=f"{os.path.dirname(__file__)}/data/training_data.parquet"):
        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT preprocessed_text, final_label
            FROM messages
            WHERE created_at <= %s
            ORDER BY created_at ASC
            """,
            (before,)
        )

        rows = cur.fetchall()
        cur.close()

        if not rows:
            logging.info(f"Aucun message avant ou à la date {before}.")
            return

        new_messages = pd.DataFrame(rows, columns=["text", "label"])

        # Conversion explicite bool -> int
        # False = 0 / True = 1
        new_messages["label"] = (new_messages["label"].astype(int))

        os.makedirs(os.path.dirname(parquet_path), exist_ok=True)

        # Si le parquet existe déjà, on conserve son contenu
        if os.path.exists(parquet_path):
            existing_messages = pd.read_parquet(parquet_path)

            all_messages = pd.concat([existing_messages, new_messages], ignore_index=True)

            # Évite de réinsérer exactement les mêmes exemples
            all_messages = all_messages.drop_duplicates(subset=["text", "label"], keep="last")

        else:
            all_messages = new_messages

        all_messages.to_parquet(parquet_path, index=False)

        logging.info(
            f"{len(new_messages)} messages anonymisés "
            f"ajoutés dans {parquet_path}."
        )


    def delete_phase_messages(self, before):
        cur = self.conn.cursor()

        cur.execute(
            """
            DELETE FROM messages
            WHERE created_at <= %s
            """,
            (before,)
        )

        deleted_count = cur.rowcount

        self.conn.commit()
        cur.close()

        logging.info(
            f"{deleted_count} messages créés avant ou à "
            f"{before} ont été supprimés."
        )




    import datetime


    def create_auth_code(self, email, code_hash, expires_at):
        cur = self.conn.cursor()

        cur.execute(
            """
            INSERT INTO auth_sessions (
                email,
                code_hash,
                code_expires_at,
                session_token_hash,
                session_expires_at
            )
            VALUES (%s, %s, %s, NULL, NULL)
            """,
            (
                email,
                code_hash,
                expires_at
            )
        )

        self.conn.commit()
        cur.close()


    def get_latest_auth_code(self, email):
        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                code_hash,
                code_expires_at
            FROM auth_sessions
            WHERE email = %s
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (email,)
        )

        row = cur.fetchone()
        cur.close()

        return row


    def activate_auth_session(
        self,
        auth_id,
        session_token_hash,
        session_expires_at
    ):
        cur = self.conn.cursor()

        cur.execute(
            """
            UPDATE auth_sessions
            SET
                session_token_hash = %s,
                session_expires_at = %s,
                code_hash = NULL,
                code_expires_at = NULL
            WHERE id = %s
            """,
            (
                session_token_hash,
                session_expires_at,
                auth_id
            )
        )

        self.conn.commit()
        cur.close()


    def get_session_by_token(self, session_token_hash):
        cur = self.conn.cursor()

        cur.execute(
            """
            SELECT
                id,
                email,
                session_expires_at
            FROM auth_sessions
            WHERE session_token_hash = %s
            LIMIT 1
            """,
            (session_token_hash,)
        )

        row = cur.fetchone()
        cur.close()

        return row


    def delete_session(self, session_token_hash):
        cur = self.conn.cursor()

        cur.execute(
            """
            DELETE FROM auth_sessions
            WHERE session_token_hash = %s
            """,
            (session_token_hash,)
        )

        self.conn.commit()
        cur.close()