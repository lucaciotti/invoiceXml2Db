import os
import sys
import glob
from pathlib import Path
from peewee import *
from datetime import datetime

from src.provider.config import Config
from src.provider.storage import RepoStorage

class DB:

    basePath = None

    def __init__(self) -> None:
        self.config = Config()
        self.repoStorage = RepoStorage()

    def getDb(self):
        path = self.config.get_conf('db', 'path')
        name = self.config.get_conf('db', 'name')
        return SqliteDatabase(RepoStorage().getFile(RepoStorage().getOrCreateSubPath(path), name+".db"))