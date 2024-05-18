import base64
import datetime
import os
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m
from src.provider.storage import RepoStorage

class docAttachmentsDTO:   

    def __init__(self, allegati):
        self.allegati = allegati

    @classmethod
    def fromXML(self, xmlObj, doc):
        allegati = []
        for node in xmlObj.getNodeList(['Allegati']):
            allegato = docAttachmentDTO.fromXML(xmlObj, node, doc)
            allegati.append(allegato)

        return allegati

class docAttachmentDTO(BaseDTO):    

    model_cls = m.DocAttachment    

    def __init__(self, doc, filetype, path, relative_path, data=None):
        self.doc = doc.db_id
        self.doc_obj = doc
        self.filetype = filetype
        self.path = path
        self.relative_path = relative_path
        self.data = data or datetime.datetime.now()

    def dbExist(self):
        try:
            record = self.model_cls.filter(doc=self.doc, relative_path=self.relative_path).get()
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
    def fromXML(self, xmlObj, xmlNode, doc):
        storage = RepoStorage()

        namefile = xmlObj.getNodeData('NomeAttachment', xmlNode)
        filetype = xmlObj.getNodeData('FormatoAttachment', xmlNode)
        descrizione = xmlObj.getNodeData('DescrizioneAttachment', xmlNode)
        file_base64 = xmlObj.getNodeData('Attachment', xmlNode)
        if file_base64 is None:
            return None
        p_iva = doc.clifor_obj.p_iva or doc.clifor_obj.c_f
        denominazione = doc.clifor_obj.denominazione.replace('/','_').replace(' ','_').replace(' ','_').replace('"', '').replace('\'', '')
        numdoc = doc.numerodoc.replace('/','_').replace(' ','_').replace(' ','_').replace('"', '').replace('\'', '')
        esercizio = doc.esercizio
    
        try:
            # filePath = os.path.join(storage.getOrCreatePath(f'attachments/{denominazione}_{p_iva}/{esercizio}/{numdoc}/')[0], namefile)
            filePath = os.path.join(storage.getOrCreatePath(f'attachments/{p_iva}/{esercizio}/{numdoc}/')[0], namefile)
        except Exception as e:
            print(str(e))

        try:
            file_content=base64.b64decode(file_base64)
            with open(filePath,"wb") as f:
                f.write(file_content)
        except Exception as e:
            print(str(e))

        
        allegato = self(doc, filetype, filePath, storage.getRelativePath(filePath))
        allegato.dto2DB()

        return allegato
    
    @classmethod
    def attachFile(self, filePath, doc, originalPath=False):
        storage = RepoStorage()

        namefile = os.path.basename(filePath)
        filetype = (os.path.splitext(namefile)[1][1:]).upper()
        descrizione = namefile

        p_iva = doc.clifor_obj.p_iva or doc.clifor_obj.c_f
        denominazione = doc.clifor_obj.denominazione.replace('/','_').replace(' ','_').replace('"', '').replace('\'', '')
        numdoc = doc.numerodoc.replace('/','_').replace(' ','_').replace('"', '').replace('\'', '')
        esercizio = doc.esercizio

        if not originalPath:
            try:
                # filePath = storage.archiveFile(f'attachments/{denominazione}_{p_iva}/{esercizio}/{numdoc}/', filePath)
                filePath = storage.archiveFile(f'attachments/{p_iva}/{esercizio}/{numdoc}/', filePath)
            except Exception as e:
                print(str(e))
            allegato = self(doc, filetype, filePath, storage.getRelativePath(filePath))
        else:
            allegato = self(doc, filetype, filePath, None)

        allegato.dto2DB()        

        return allegato

             