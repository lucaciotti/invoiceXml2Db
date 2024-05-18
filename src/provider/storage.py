
import os
import shutil
import sys
import glob
from pathlib import Path
from datetime import datetime

class RepoStorage:

    basePath = None

    def __init__(self) -> None:
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.basePath = Path(os.path.dirname(sys.executable))
        else:
            # self.basePath = Path(os.path.dirname(sys.executable)).parent.absolute()
            # if '.venv' in self.basePath:
            self.basePath = Path(os.path.dirname(sys.executable)).parent.parent.absolute()

        # DIR_PATH = Path(typer.get_app_dir(__app_name__))
        # DIR_PATH = Path(os.path.dirname(sys.executable))
        # DIR_PATH = Path(os.path.dirname(sys.modules['__main__'].__file__)).parent.absolute()

    def getBasePath(self):
        return self.basePath
    
    def getOrCreateSubPath(self, subDir):
        path = Path(os.path.join(self.basePath, subDir))
        try:
            path.mkdir(exist_ok=True, parents=True)
        except OSError:
            return None
        
        return path
    
    def getOrCreatePath(self, path, create=True):
        if not os.path.isabs(path):
            path = Path(os.path.join(self.basePath, path))
        else:
            path = Path(path)
        exist = path.exists()
        if not exist and create:
            try:
                path.mkdir(exist_ok=True, parents=True)
            except OSError:
                return None, exist
        return path, exist
    
    def getFile(self, path, filename):
        return Path(os.path.join(path, filename))
    
    def getRelativePath(self, path):
        return os.path.relpath(path, self.basePath)
    
    def checkFile(self, file, **kwargs) -> int:
        if os.path.isabs(file):
            file = Path(file)
        else:
            path = Path(self.basePath) if 'path' not in kwargs else Path(kwargs['path'])
            file = Path(os.path.join(path, file))

        if not file.exists():
            if 'create_file' in kwargs:
                return file.touch(exist_ok=True)
            return False
        return True
    
    def archiveFile(self, subDir, file, move=False, timestamp=True):
        path = self.getOrCreateSubPath(subDir)
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename, file_ext = self._getFileExt(os.path.basename(file))
        if timestamp:
            filename = Path(os.path.join(path, '{0}_{1}{2}'.format(filename, ts, file_ext)))
        else:
            filename = Path(os.path.join(path, '{0}{1}'.format(filename, file_ext)))

        if move:
            os.rename(file, filename)
        else:
            shutil.copyfile(file, filename)
        return filename

    def _getFileExt(self, file):
        return os.path.splitext(file)
    
    def getUserDownloadFolder(self):
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    
    def getAllFilesInFolder(self, path, **kwargs):
        # * means all if need specific format then *.csv
        pattern = kwargs['pattern'] if 'pattern' in kwargs else '*'
        ct_after = kwargs['ct_after'] if 'ct_after' in kwargs else None
        list_of_files = sorted(glob.glob(os.path.join(path, pattern)), key=os.path.getctime)
        if ct_after and isinstance(ct_after, datetime):
            list_of_files = [file for file in list_of_files if datetime.fromtimestamp(os.path.getctime(file)) > ct_after]
        return list_of_files

    def getLatestFileInFolder(self, path, **kwargs):
        # * means all if need specific format then *.csv
        pattern = kwargs['pattern'] if 'pattern' in kwargs else '*'
        list_of_files = glob.glob(os.path.join(path, pattern))
        return max(list_of_files, key=os.path.getctime)

    def getTmpFilesCount(self, path):
        notTempFiles = [i for i in os.listdir(path) if (i.endswith('.tmp') or i.endswith('.crdownload'))]
        return len(notTempFiles)
