import datetime
from src.dto.base import BaseDTO
from src.dto.clifor import cliforDTO, sedecliforDTO
from src.models import fatturaEl as m

class pagamentiDTO:   

    def __init__(self, pagamenti):
        self.pagamenti = pagamenti

    @classmethod
    def fromXML(self, xmlObj, doc):
        pagamenti = []
        condizioniPagamento = xmlObj.getNodeData('DatiPagamento/CondizioniPagamento')
        for node in xmlObj.getNodeList('DatiPagamento/DettaglioPagamento'):
            pagamento = pagamentoDTO.fromXML(xmlObj, node, doc, condizioniPagamento)
            pagamenti.append(pagamento)

        return pagamenti


class pagamentoDTO(BaseDTO):    

    model_cls = m.Pagamenti    

    def __init__(self, doc, cod_condizione_pag, descr_condizione_pag, mod_pag, data_scad, importo_pag, banca, iban, bic):
        self.doc = doc.db_id
        self.doc_obj = doc
        self.dare = doc.acquisto
        self.avere = doc.vendita
        self.cod_condizione_pag = cod_condizione_pag
        self.descr_condizione_pag = descr_condizione_pag or ''
        self.mod_pag = mod_pag
        self.data_scad = data_scad or datetime.datetime.now()
        self.importo_pag = importo_pag or 0
        self.banca = banca
        self.iban = iban
        self.bic = bic

    def dbExist(self):
        try:
            record = self.model_cls.filter(doc=self.doc, data_scad=self.data_scad, mod_pag=self.mod_pag).get()
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
    def fromXML(self, xmlObj, xmlNode, doc, cod_condizione_pag):
        descr_condizione_pag = ''
        mod_pag = xmlObj.getNodeData('ModalitaPagamento', xmlNode)
        data_scad = xmlObj.getNodeData('DataScadenzaPagamento', xmlNode)
        try:
            data_scad = datetime.datetime.strptime(data_scad, '%Y-%m-%d') if data_scad else doc.data
        except Exception as e:
            print(str(e))
            data_scad = doc.data
        importo_pag = xmlObj.getNodeData('ImportoPagamento', xmlNode)
        banca = xmlObj.getNodeData('IstitutoFinanziario', xmlNode)
        iban = xmlObj.getNodeData('IBAN', xmlNode)
        bic = xmlObj.getNodeData('BIC', xmlNode)       
        
        pagamento = self(doc, cod_condizione_pag, descr_condizione_pag, mod_pag, data_scad, importo_pag, banca, iban, bic)
        pagamento.dto2DB()

        return pagamento