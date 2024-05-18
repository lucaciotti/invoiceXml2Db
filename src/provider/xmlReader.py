import os
from pathlib import Path
from xml.dom.minidom import parse, parseString

import typer

from src.provider.notifier import Notifier


class XmlReader:
    notification = None
    xmldom = None

    def __init__(self, file):
        file_check = self._check_file(file)
        self.notification = Notifier()

        if file_check != 1:
            typer.secho(
                f'XLM file check failed',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        try:
            self.xmldom = parse(file)
        except Exception as e_parse:
            # self.notification.send("Xml load.", "Errore! Cosultare i log.")
            if "not well-formed" in str(e_parse):
                try:
                    f = open(file, "r", encoding="utf-8-sig")
                    ff = f.read()
                    if 'ï»¿' in ff:
                        fff=ff.replace('ï»¿', '')
                        self.xmldom = parseString(fff)
                    else:
                        typer.secho(
                            f'Failed Xml standard load: ' + str(e_parse),
                            fg=typer.colors.RED,
                        )
                        raise e_parse
                except Exception as e:
                    # self.notification.send("Xml load.", "Errore! Cosultare i log.")
                    typer.secho(
                        f'Failed Xml without-bom load: ' + str(e),
                        fg=typer.colors.RED,
                    )
                    raise e
            else:
                typer.secho(
                    f'Failed Xml standard load: ' + str(e_parse),
                    fg=typer.colors.RED,
                )
                raise e_parse

    def _check_file(self, file) -> int:
        if os.path.isabs(file):
            self.fileXls = Path(file)
        else:
            # path = Path(self.CONFIG_DIR_PATH).parent.absolute()
            path = Path(self.DIR_PATH)
            self.fileXls = Path(os.path.join(path, "xlsUpload", file))

        if not self.fileXls.exists():
            return -1
        return 1
    
    def _checkNodePath(self, nodePath):
        # Check nodeName or Path given by user
        if isinstance(nodePath, str):
            if '/' in nodePath:
                nodePath=nodePath.replace(' ', '').split('/')
            else:
                nodePath = [nodePath]
        if isinstance(nodePath, list):
            return nodePath
    
    def getNode(self, nodePath, nodeRoot=None):
        nodePath = self._checkNodePath(nodePath)
        nodeName = nodePath.pop(0)
        node = None
        if nodeRoot is None:
            nodeRoot = self.xmldom
        try:
            nodes = nodeRoot.getElementsByTagName(nodeName)
            if len(nodes)==1:
                node = nodes[0]        
                if len(nodePath)>0:
                    return self.getNode(nodePath, node)
            return node
        except Exception as e:
            print(e)
        
    def getNodeList(self, nodePath, nodeRoot=None):
        nodePath = self._checkNodePath(nodePath)
        nodeName = nodePath.pop(0)
        nodeList = []
        if nodeRoot is None:
            nodeRoot = self.xmldom
        try:
            nodes = nodeRoot.getElementsByTagName(nodeName)
            if len(nodes)==1 and len(nodePath)>0:
                    return self.getNodeList(nodePath, nodes[0])
            if len(nodes)>0:
                nodeList = nodes
            return nodeList
        except Exception as e:
            print(e)

    def getNodeName(self, nodePath, nodeRoot=None):
        node = self.getNode(nodePath, nodeRoot)
        return node.nodeName if node is not None else None

    def getNodeData(self, nodePath, nodeRoot=None):
        node = self.getNode(nodePath, nodeRoot)
        try:
            return node.firstChild.data if node is not None else None
        except Exception as e:
            print(f'Error XmlNode {nodePath} data not found!')
    
