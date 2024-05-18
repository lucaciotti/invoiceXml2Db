from peewee import *
import datetime
from src.models.base import BaseModel
from src.models.fatturaEl.clifor import CliFor, SediCliFor


class Doc(BaseModel):
    clifor = ForeignKeyField(CliFor, backref='docs')
    sedeclifor = ForeignKeyField(SediCliFor)
    tipodoc = CharField(null=True)
    numerodoc = CharField(null=True)
    acquisto = BooleanField(default=False)
    vendita = BooleanField(default=False)
    data = DateTimeField(default=datetime.datetime.now)
    esercizio = IntegerField(null=True)
    aliquota_cassa = DoubleField(default=0)
    imposta_cassa = DoubleField(default=0)
    totale = DoubleField(default=0)

class DocRow(BaseModel):
    doc = ForeignKeyField(Doc, backref='rows')
    numerolinea = IntegerField(default=0)
    codart = CharField(null=True)
    tipocodice = CharField(null=True)
    descrizione = CharField(null=True)
    qta = DoubleField(default=0)
    um = CharField(default='')
    prz_unit = DoubleField(default=0)
    prz_tot = DoubleField(default=0)
    aliquotaIVA = DoubleField(default=0)

class DocAliquota(BaseModel):
    doc = ForeignKeyField(Doc, backref='aliquote')
    imponibile = DoubleField(default=0)
    aliquotaIVA = DoubleField(default=0)
    imposta = DoubleField(default=0)
    codIVA = CharField(null=True)
    rifnorma = CharField(null=True)
    