import datetime
import os
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m

class xmlFileDTO(BaseDTO):    

    model_cls = m.XmlFile    

    def __init__(self, name, dt_file_ct, doc, dt_last_import=None):
        self.name = name
        self.dt_last_import = dt_last_import or datetime.datetime.now()
        self.dt_file_ct = dt_file_ct or datetime.datetime.now()
        self.doc = doc.db_id
        self.attive = doc.vendita
        self.passive = doc.acquisto

    def dbExist(self):
        try:
            record = self.model_cls.filter(name=self.name, dt_file_ct=self.dt_file_ct).get()
            if record:
                return record.id, record
            else:
                return None, None
        except self.model_cls.DoesNotExist:
            return None, None

    def _buildDataDb(self):
        data = self.__dict__
        self.data_db = data

    @classmethod
    def fromFile(self, xmlFile, doc):
        name = os.path.basename(xmlFile)
        dt_file_ct = datetime.datetime.fromtimestamp(os.path.getctime(xmlFile))
        
        xmlFileDTO = self(name, dt_file_ct, doc)
        xmlFileDTO.dto2DB()

        return xmlFileDTO