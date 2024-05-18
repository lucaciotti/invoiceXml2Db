import datetime
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m

class docDTO(BaseDTO):    

    model_cls = m.Doc    

    def __init__(self, tipodoc, numerodoc, acquisto, vendita, data, esercizio, aliquota_cassa, imposta_cassa, totale, clifor, sedeclifor):
        self.tipodoc = tipodoc
        self.numerodoc = numerodoc
        self.acquisto = acquisto
        self.vendita = vendita
        self.data = data
        self.esercizio = esercizio
        self.aliquota_cassa = aliquota_cassa or 0
        self.imposta_cassa = imposta_cassa or 0
        self.totale = totale or 0
        self.clifor = clifor.db_id if clifor is not None else None
        self.sedeclifor = sedeclifor.db_id if sedeclifor is not None else None
        self.clifor_obj = clifor
        self.sedeclifor_obj = sedeclifor

    def dbExist(self):
        try:
            record = self.model_cls.filter(clifor=self.clifor, data=self.data, numerodoc=self.numerodoc).get()
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
    def fromXML(self, xmlObj, create=True):
        tipodoc = xmlObj.getNodeData('DatiGeneraliDocumento/TipoDocumento')
        numerodoc = xmlObj.getNodeData('DatiGeneraliDocumento/Numero')
        idCommittente = xmlObj.getNodeData('CessionarioCommittente/IdCodice') or xmlObj.getNodeData('CessionarioCommittente/CodiceFiscale')
        acquisto = idCommittente==self.config.get_conf('ditta', 'p_iva')
        vendita = xmlObj.getNodeData('CedentePrestatore/IdCodice')==self.config.get_conf('ditta', 'p_iva')
        data = datetime.datetime.strptime(xmlObj.getNodeData('DatiGeneraliDocumento/Data'), '%Y-%m-%d')
        esercizio = data.year        
        aliquota_cassa = xmlObj.getNodeData('DatiGeneraliDocumento/AlCassa')
        imposta_cassa = xmlObj.getNodeData('DatiGeneraliDocumento/ImportoContributoCassa')
        totale = xmlObj.getNodeData('DatiGeneraliDocumento/ImportoTotaleDocumento')

        if not acquisto and not vendita:
            raise Exception('Documento non inerente alla ditta')

        if not create:
            return self(tipodoc, numerodoc, acquisto, vendita, data, esercizio, 
                    aliquota_cassa, imposta_cassa, totale, None, None)
        
        clifor = cliforDTO.fromXML(xmlObj, acquisto)
        sedeclifor = sedecliforDTO.fromXML(xmlObj, acquisto, clifor)
        
        
        doc = self(tipodoc, numerodoc, acquisto, vendita, data, esercizio, 
                    aliquota_cassa, imposta_cassa, totale, clifor, sedeclifor)
        doc.dto2DB()

        return doc