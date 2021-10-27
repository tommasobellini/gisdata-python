import os

from peewee import Model, MySQLDatabase, CharField, DecimalField, DateField, ForeignKeyField

from database import mysql_db, proxy


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = proxy


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
