import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
import logging



class Postgres_DB:
    def __init__(self, sql_file_path):
        self.sql_file_path = sql_file_path
        self._connect()

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
            

