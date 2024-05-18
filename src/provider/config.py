import configparser

from .storage import RepoStorage

class Config:
    repoStorage = None
    path = None
    file = None
    config = None

    def __init__(self):
        self.repoStorage = RepoStorage()
        self.path = self.repoStorage.getBasePath()
        self.file = self.repoStorage.getFile(self.path, "config.ini")
        file_exist = self.repoStorage.checkFile(self.file, path=self.file)

        self.config = configparser.ConfigParser()
        self.config.read(self.file)

    def get_conf(self, section: str, key: str):
        return self.config[section][key]

    def print_conf(self):
        return print({section: dict(self.config[section]) for section in self.config.sections()})
