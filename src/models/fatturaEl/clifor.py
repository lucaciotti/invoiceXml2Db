from peewee import *
import datetime
from src.models.base import BaseModel


class CliFor(BaseModel):
    denominazione = CharField(null=True)
    p_iva = CharField(null=True)
    c_f = CharField(null=True)

class SediCliFor(BaseModel):
    clifor = ForeignKeyField(CliFor, backref='sedi')
    indirizzo = CharField(null=True)
    cap = IntegerField(null=True)
    comune = CharField(null=True)
    provincia = CharField(null=True)
    nazione = CharField(null=True)