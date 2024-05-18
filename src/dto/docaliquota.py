import datetime
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m

class docAliquoteDTO:   

    def __init__(self, docaliquote):
        self.docaliquote = docaliquote

    @classmethod
    def fromXML(self, xmlObj, doc):
        docaliquote = []
        for node in xmlObj.getNodeList('DatiBeniServizi/DatiRiepilogo'):
            dociva = docAliquotaDTO.fromXML(xmlObj, node, doc)
            docaliquote.append(dociva)

        return docaliquote


class docAliquotaDTO(BaseDTO):    

    model_cls = m.DocAliquota    

    def __init__(self, doc, imponibile, aliquotaIVA, imposta, codIVA, rifnorma):
        self.doc = doc.db_id
        self.doc_obj = doc
        self.imponibile = imponibile or 0
        self.aliquotaIVA = aliquotaIVA or 0
        self.imposta = imposta or 0
        self.codIVA = codIVA
        self.rifnorma = rifnorma

    def dbExist(self):
        try:
            record = self.model_cls.filter(doc=self.doc, aliquotaIVA=self.aliquotaIVA).get()
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
        imponibile = xmlObj.getNodeData('ImponibileImporto', xmlNode)
        aliquotaIVA = xmlObj.getNodeData('AliquotaIVA', xmlNode)
        imposta = xmlObj.getNodeData('Imposta', xmlNode)     
        codIva = xmlObj.getNodeData('Natura', xmlNode)     
        rifnorma = xmlObj.getNodeData('RiferimentoNormativo', xmlNode)     
        
        dociva = self(doc, imponibile, aliquotaIVA, imposta, codIva, rifnorma)
        dociva.dto2DB()

        return dociva