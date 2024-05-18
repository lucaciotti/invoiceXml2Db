from peewee import *
import datetime
from src.models.base import BaseModel
from src.models.fatturaEl.doc import Doc


class Pagamenti(BaseModel):
    doc = ForeignKeyField(Doc, backref='pagamenti')
    dare = BooleanField(default=False)
    avere = BooleanField(default=False)
    cod_condizione_pag = CharField(null=True)
    descr_condizione_pag = CharField(null=True)
    mod_pag = CharField(null=True)
    data_scad = DateTimeField(default=datetime.datetime.now)
    importo_pag = DoubleField(default=0)
    banca = CharField(null=True)
    iban = CharField(null=True)
    bic = CharField(null=True)