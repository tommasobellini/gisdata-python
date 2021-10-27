import logging
import os
import peewee as pw
from peewee import MySQLDatabase

logging.basicConfig(level=logging.INFO)

logging.info("Inizializzando database..")
mysql_db = MySQLDatabase(os.environ.get('MYSQL_DATABASE'), user=os.environ.get('MYSQL_USER'),
                         password=os.environ.get('MYSQL_PASSWORD'),
                         host=os.environ.get('DB_HOST'), port=int(os.environ.get('DB_PORT')))
proxy = pw.Proxy()
proxy.initialize(mysql_db)
logging.info("Inizializzazione database avvenuta con successo!")
