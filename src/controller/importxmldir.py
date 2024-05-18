from pathlib import Path
from src.__main__ import CSVLOGGER
from src.dto.docaliquota import docAliquoteDTO
from src.provider.config import Config
from src.provider.notifier import Notifier
from src.provider.storage import RepoStorage
from src.models import fatturaEl as m

from src.dto.allegati import docAttachmentDTO, docAttachmentsDTO
from src.dto.doc import docDTO
from src.dto.docrow import docRowsDTO
from src.dto.pagamenti import pagamentiDTO
from src.dto.xmlFile import xmlFileDTO
from src.provider.xmlReader import XmlReader


class ImportXmlDir:

    def __init__(self) -> None:
        self.config = Config()
        self.repoStorage = RepoStorage()
        self.notification = Notifier()
    
    def autoImportPassive(self, skip_ct_filter=False):
        try:
            config_path = self.config.get_conf('invoice', 'xml_fattura_passive')
            if config_path in (None, ''):
                print(f'Path Fatture Passive non inserito!')
                CSVLOGGER.addLogRow('AutoImport', '', '', f'Path Fatture Attive non inserito!')
                return
            path, _ = self.repoStorage.getOrCreatePath(config_path)
            if not skip_ct_filter:
                lastCtFileImported = m.XmlFile.getLastDtFileCt_passive()
                files = self.repoStorage.getAllFilesInFolder(path, pattern='*.xml', ct_after=lastCtFileImported)
            else:
                files = self.repoStorage.getAllFilesInFolder(path, pattern='*.xml')
            
            archive_path = None
            if eval(self.config.get_conf('invoice', 'archive_processed')):
                   archive_path, _ = self.repoStorage.getOrCreatePath(config_path+'/processed')
            
            if len(files)>0:
                self.autoImport(files, archive_path)
                self.notification.send("AutoImport Passive", f"Processate {len(files)} fatture!")
        except Exception as e:
            print(e)
            CSVLOGGER.addLogRow('Error', '', '', str(e))
    
    def autoImportAttive(self, skip_ct_filter=False):
        try:
            config_path = self.config.get_conf('invoice', 'xml_fattura_attive')
            if config_path in (None, ''):
                print(f'Path Fatture Attive non inserito!')
                CSVLOGGER.addLogRow('AutoImport', '', '', f'Path Fatture Attive non inserito!')
                return            
            path, _ = self.repoStorage.getOrCreatePath(config_path)
            if not skip_ct_filter:
                lastCtFileImported = m.XmlFile.getLastDtFileCt_passive()
                files = self.repoStorage.getAllFilesInFolder(path, pattern='*.xml', ct_after=lastCtFileImported)
            else:
                files = self.repoStorage.getAllFilesInFolder(path, pattern='*.xml')
            
            archive_path = None
            if eval(self.config.get_conf('invoice', 'archive_processed')):
                   archive_path, _ = self.repoStorage.getOrCreatePath(config_path+'/processed')
            
            if len(files)>0:
                self.autoImport(files, archive_path)
                self.notification.send("AutoImport Attive", f"Processate {len(files)} fatture!")
        except Exception as e:
            print(e)
            CSVLOGGER.addLogRowAndWrite('Error', '', '', str(e))

    def autoImport(self, files, archive_path=None):
        try:
            tot_files = len(files)
            for pos, file in enumerate(files):
                pos = pos+1
                if m.XmlFile.isFileProcessed(file):
                    print(f'Il file "{file}" è già stato processato!')
                    doc = docDTO.fromXML(xml, create=False)
                    if archive_path:
                        self.repoStorage.archiveFile(f'{archive_path}/{doc.esercizio}/', file)
                    CSVLOGGER.addLogRow('AutoImport', '', '', f'{pos}/{tot_files} -> "{file}" già stato processato precedentemente!')
                    continue
                print(f'==> {pos}/{tot_files} "{file}"')
                CSVLOGGER.addLogRow('AutoImport', '', '', f'{pos}/{tot_files} -> "{file}"')

                try:
                    xml=XmlReader(file)                
                except Exception as e:
                    CSVLOGGER.addLogRow('Error', '', '', str(e))
                    continue

                try:
                    doc = docDTO.fromXML(xml)
                except Exception as e:
                    if str(e)=='Documento non inerente alla ditta':
                        CSVLOGGER.addLogRow('Error', '', '', str(e))
                        continue
                    else:
                        self.notification.send("Xml load.", "Errore! Cosultare i log.")
                        CSVLOGGER.addLogRow('Error', '', '', str(e))
                        break

                docrows = docRowsDTO.fromXML(xml, doc)
                docaliquote = docAliquoteDTO.fromXML(xml, doc)
                pagamenti = pagamentiDTO.fromXML(xml, doc)
                allegati = docAttachmentsDTO.fromXML(xml, doc)
                if eval(self.config.get_conf('invoice', 'archive_xml_to_attachments')):
                    allegatoXML = docAttachmentDTO.attachFile(file, doc)
                xmlFile = xmlFileDTO.fromFile(file, doc)

                # Archivio i file processati in una sub directory (se configurato)
                if archive_path:
                    file_archive = self.repoStorage.archiveFile(f'{archive_path}/{doc.esercizio}/', Path(file), move=True, timestamp=False)
                    allegatoXML = docAttachmentDTO.attachFile(file_archive, doc, originalPath=True)

        except Exception as e:
            self.notification.send("Xml load.", "Errore! Cosultare i log.")
            print(e)
            CSVLOGGER.addLogRow('Error', '', '', str(e))

    def manualImport(self, xmlDirPath):        
        try:
            path, exists = self.repoStorage.getOrCreatePath(xmlDirPath, create=False)
            if not exists:
                raise Exception(f'La Directory {xmlDirPath} non esiste')
            files = self.repoStorage.getAllFilesInFolder(path, pattern='*.xml')
            tot_files = len(files)
            for pos, file in enumerate(files):
                pos = pos+1
                if m.XmlFile.isFileProcessed(file):
                    print(f'--> Il file "{file}" è già stato processato!')
                    CSVLOGGER.addLogRow('ManualImport', '', '', f'{pos}/{tot_files} -> "{file}" già stato processato precedentemente!')
                    continue
                print(f'==> {pos}/{tot_files} "{file}"')
                CSVLOGGER.addLogRow('ManualImport', '', '', f'{pos}/{tot_files} -> "{file}"')
                
                try:
                    xml=XmlReader(file)                
                except Exception as e:
                    CSVLOGGER.addLogRow('Error', '', '', str(e))
                    continue

                try:
                    doc = docDTO.fromXML(xml)
                except Exception as e:
                    if str(e)=='Documento non inerente alla ditta':
                        CSVLOGGER.addLogRow('Error', '', '', str(e))
                        continue
                    else:
                        self.notification.send("Xml load.", "Errore! Cosultare i log.")
                        CSVLOGGER.addLogRow('Error', '', '', str(e))
                        break

                docrows = docRowsDTO.fromXML(xml, doc)
                docaliquote = docAliquoteDTO.fromXML(xml, doc)
                pagamenti = pagamentiDTO.fromXML(xml, doc)
                allegati = docAttachmentsDTO.fromXML(xml, doc)
                if eval(self.config.get_conf('invoice', 'archive_xml_to_attachments')):
                    allegatoXML = docAttachmentDTO.attachFile(file, doc)
                xmlFile = xmlFileDTO.fromFile(file, doc)
                
                allegatoXML = docAttachmentDTO.attachFile(file, doc, originalPath=True)
            
            if len(files)>0:
                self.notification.send("ManualImport", f"Processate {len(files)} fatture!")
        except Exception as e:
            print(e)
            CSVLOGGER.addLogRow('Error', '', '', str(e))