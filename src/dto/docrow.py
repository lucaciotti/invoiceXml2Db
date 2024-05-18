import datetime
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m

class docRowsDTO:   

    def __init__(self, docrows):
        self.docrows = docrows

    @classmethod
    def fromXML(self, xmlObj, doc):
        docrows = []
        for node in xmlObj.getNodeList('DatiBeniServizi/DettaglioLinee'):
            docrow = docRowDTO.fromXML(xmlObj, node, doc)
            docrows.append(docrow)

        return docrows


class docRowDTO(BaseDTO):    

    model_cls = m.DocRow    

    def __init__(self, doc,numerolinea, codart, tipocodice, descrizione, qta, um, prz_unit, prz_tot, aliquotaIVA):
        self.doc = doc.db_id
        self.doc_obj = doc
        self.numerolinea = numerolinea or 0
        self.codart = codart
        self.tipocodice = tipocodice
        self.descrizione = descrizione
        self.qta = qta or 0
        self.um = um or ''
        self.prz_unit = prz_unit or 0
        self.prz_tot = prz_tot or 0
        self.aliquotaIVA = aliquotaIVA or 0

    def dbExist(self):
        try:
            record = self.model_cls.filter(doc=self.doc, numerolinea=self.numerolinea).get()
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
        numerolinea = xmlObj.getNodeData('NumeroLinea', xmlNode)
        codart = xmlObj.getNodeData('CodiceValore', xmlNode)
        tipocodice = xmlObj.getNodeData('CodiceTipo', xmlNode)
        descrizione = xmlObj.getNodeData('Descrizione', xmlNode)
        qta = xmlObj.getNodeData('Quantita', xmlNode)
        um = xmlObj.getNodeData('UnitaMisura', xmlNode)
        prz_unit = xmlObj.getNodeData('PrezzoUnitario', xmlNode)
        prz_tot = xmlObj.getNodeData('PrezzoTotale', xmlNode)
        aliquotaIVA = xmlObj.getNodeData('AliquotaIVA', xmlNode)        
        
        docrow = self(doc, numerolinea, codart, tipocodice, descrizione, qta, um, prz_unit, prz_tot, aliquotaIVA)
        docrow.dto2DB()

        return docrow