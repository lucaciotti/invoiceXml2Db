import os
import sys
from pathlib import Path
from peewee import *
import datetime
from src.provider.db import DB
from src.provider.storage import RepoStorage

db = DB().getDb()

class BaseModel(Model):
    updated_at = DateTimeField()
    
    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    
    @classmethod
    def update(cls, *args, **kwargs):
        kwargs['updated_at'] = datetime.datetime.now()
        return super(BaseModel, cls).update(*args, **kwargs)
