
from src.provider.config import Config


class BaseDTO:
    db_id = None
    data_db = None

    model_cls = None
    config = Config()

    def dbExist(self):
        pass
    
    def _buildDataDb(self):
        pass

    def exist(self):
        return True if self.db_id is not None else False
    
    def getDbFieldsList(self):
        return [key for key in self.data_db.keys() if key != 'db_id']


    def dto2DB(self):
        try:
            self._buildDataDb()
            self.data_db = {el:self.data_db[el]  for el in self.data_db if (el not in ['data_db', 'db_id',]) and not el.endswith('_obj')}
            if self.db_id is None:
                self.db_id, _ = self.dbExist()

            if self.db_id is None:
                record, created = self.model_cls.get_or_create(**self.data_db)
                self.db_id = record.id
            else:
                self.model_cls.update(**self.data_db).where(self.model_cls.id==self.db_id).execute()
        except Exception as e:
            raise Exception("Errore nel salvataggio: {}".format(str(e)))
            