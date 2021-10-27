import os

from peewee import Model, MySQLDatabase, CharField, DecimalField, DateField, ForeignKeyField

mysql_db = MySQLDatabase(os.environ.get('MYSQL_DATABASE'), user=os.environ.get('MYSQL_USER'), password=os.environ.get('MYSQL_PASSWORD'),
                         host='localhost', port=3306)


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db


class Utenti(BaseModel):
    """
    Modello per tabella Utenti
    """
    nome = CharField()
    primo_deposito = DecimalField(decimal_places=2)
    saldo = DecimalField(decimal_places=2)


class Operazioni(BaseModel):
    """
    Modello per tabella Operazioni
    """
    utente_id = ForeignKeyField(Utenti)
    giorno = DateField()
    ammontare = DecimalField(decimal_places=2)
