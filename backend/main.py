from modules.Database import Postgres_DB
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import sys
import os


Postgres_DB(sql_file_path=f"{os.path.dirname(__file__)}/modules/data/db.sql").create_tables_if_not_exist()



