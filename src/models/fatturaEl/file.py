from peewee import *
import datetime

from src.models.base import BaseModel
from src.models.fatturaEl.doc import Doc


class DocAttachment(BaseModel):
    doc = ForeignKeyField(Doc, backref='files')
    filetype = CharField(null=True)
    path = CharField(null=True)
    relative_path = CharField(null=True)
    data = DateTimeField(default=datetime.datetime.now)