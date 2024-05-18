import os
from peewee import *
import datetime

from src.models.base import BaseModel
from src.models.fatturaEl.doc import Doc


class XmlFile(BaseModel):
    name = CharField(null=True)
    dt_last_import = DateTimeField(default=datetime.datetime.now)
    dt_file_ct = DateTimeField(default=datetime.datetime.now)
    doc = ForeignKeyField(Doc, backref='xmlfile')
    attive = BooleanField(default=False)
    passive = BooleanField(default=False)

    @classmethod
    def getLastDtFileCt_attive(self):
        return self.select(fn.MAX(self.dt_file_ct)).where(self.attive==True).scalar()   
    
    @classmethod
    def getLastDtFileCt_passive(self):
        return self.select(fn.MAX(self.dt_file_ct)).where(self.passive==True).scalar() 
    
    @classmethod
    def isFileProcessed(self, xmlFile):
        return (self.select().where(self.name==os.path.basename(xmlFile))).exists()