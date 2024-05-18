import csv
from datetime import datetime

from .storage import RepoStorage

class csvLogger:
    repoStorage = None
    path = None
    file = None

    header = ['datatime', 'operation', 'info']
    rows = []

    def __init__(self):
        self.repoStorage = RepoStorage()
        self.rows = []
        self._init_file()

    def addLogRowAndWrite(self, operation, entity, sku, data_info):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        row = [date_time, operation, data_info]
        with open(self.file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(row)

    def addLogRow(self, operation, entity, sku, data_info):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        self.rows.append([date_time, operation, data_info])

    def write_csv_rows(self):
        with open(self.file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for row in self.rows:
                writer.writerow(row)
        self.rows = []

    def _init_file(self) -> int:
        self.path = self.repoStorage.getOrCreateSubPath('LOG')
        self.file = self.repoStorage.getFile(self.path, 'log.csv')
        
        if not self.repoStorage.checkFile(self.file, path=self.path):
            self._write_csv_header()

        return True

    def _write_csv_header(self):
        with open(self.file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(self.header)

    def moveFile(self):
        self.repoStorage.archiveFile('LOG', self.file, move=True)
