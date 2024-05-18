import datetime
from src.dto.base import BaseDTO
from src.models import fatturaEl as m

class cliforDTO(BaseDTO):    

    model_cls = m.CliFor    

    def __init__(self, denominazione, p_iva, c_f):
        self.denominazione = denominazione
        self.p_iva = p_iva
        self.c_f = c_f

    def dbExist(self):
        try:
            record = self.model_cls.filter(p_iva=self.p_iva).get()
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
    def fromXML(self, xmlObj, isAcquisto):
        if isAcquisto:
            denominazione = xmlObj.getNodeData('CedentePrestatore/Denominazione')
            nome = xmlObj.getNodeData('CedentePrestatore/Nome')
            cognome = xmlObj.getNodeData('CedentePrestatore/Cognome')
            p_iva = xmlObj.getNodeData('CedentePrestatore/IdCodice')
            c_f = xmlObj.getNodeData('CedentePrestatore/CodiceFiscale')
            if denominazione is None and (nome is not None or cognome is not None):
                denominazione = '{0} {1}'.format(nome, cognome)
            if denominazione is None:
                raise Exception('Denominazione Fornitore non trovata')
            if c_f is None:
                c_f = p_iva
            if p_iva is None and c_f is not None:
                p_iva = c_f
            if p_iva is None:
                p_iva = denominazione
        else:
            denominazione = xmlObj.getNodeData('CessionarioCommittente/Denominazione')
            nome = xmlObj.getNodeData('CessionarioCommittente/Nome')
            cognome = xmlObj.getNodeData('CessionarioCommittente/Cognome')
            p_iva = xmlObj.getNodeData('CessionarioCommittente/IdCodice')
            c_f = xmlObj.getNodeData('CessionarioCommittente/CodiceFiscale')  
            if denominazione is None and (nome is not None or cognome is not None):
                denominazione = '{0} {1}'.format(nome, cognome)
            if denominazione is None:
                raise Exception('Denominazione Cliente non trovata')
            if c_f is None:
                c_f = p_iva
            if p_iva is None and c_f is not None:
                p_iva = c_f
            if p_iva is None:
                p_iva = denominazione

        clifor = self(denominazione, p_iva, c_f)
        # sono obbligato a salvare il cliente per poter avere l'id per poi creare la sede
        clifor.dto2DB()        
        return clifor
    
class sedecliforDTO(BaseDTO):    

    model_cls = m.SediCliFor    

    def __init__(self, clifor, indirizzo, cap, comune, provincia, nazione):
        self.clifor = clifor.db_id
        self.clifor_obj = clifor
        self.indirizzo = indirizzo
        self.cap = int(cap) if cap else None
        self.comune = comune
        self.provincia = provincia
        self.nazione = nazione

    def dbExist(self):
        try:
            record = self.model_cls.filter(clifor=self.clifor, indirizzo=self.indirizzo, cap=self.cap).get()
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
    def fromXML(self, xmlObj, isAcquisto, clifor):
        if isAcquisto:
            indirizzo = xmlObj.getNodeData('CedentePrestatore/Indirizzo')
            cap = xmlObj.getNodeData('CedentePrestatore/CAP')
            comune = xmlObj.getNodeData('CedentePrestatore/Comune')
            provincia = xmlObj.getNodeData('CedentePrestatore/Provincia')
            nazione = xmlObj.getNodeData('CedentePrestatore/Nazione')
        else:
            indirizzo = xmlObj.getNodeData('CessionarioCommittente/Indirizzo')
            cap = xmlObj.getNodeData('CessionarioCommittente/CAP')
            comune = xmlObj.getNodeData('CessionarioCommittente/Comune')
            provincia = xmlObj.getNodeData('CessionarioCommittente/Provincia')
            nazione = xmlObj.getNodeData('CessionarioCommittente/Nazione') 

        clifor = clifor
        sedeclifor = self(clifor, indirizzo, cap, comune, provincia, nazione)
        # sono obbligato a salvare il cliente per poter avere l'id per poi creare la sede
        sedeclifor.dto2DB()        
        return sedeclifor