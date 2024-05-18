import sys
import typer
from notifypy import Notify
from typing import Optional
from pathlib import Path

from src import __app_name__, __version__
from src.__main__ import CSVLOGGER
from src.controller.importxmldir import ImportXmlDir
from src.dto.allegati import docAttachmentDTO, docAttachmentsDTO
from src.dto.doc import docDTO
from src.dto.docrow import docRowsDTO
from src.dto.pagamenti import pagamentiDTO
from src.dto.xmlFile import xmlFileDTO
from src.provider.config import Config
from src.models import fatturaEl as m
from src.provider.notifier import Notifier
from src.provider.storage import RepoStorage
from src.provider.xmlReader import XmlReader

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            typer.echo('running in a PyInstaller bundle')
        else:
            typer.echo('running in a normal Python process')
        raise typer.Exit()

def _config_check(value: bool) -> None:
    if value:
        config = Config()
        typer.secho(f"The Config file contains:", fg=typer.colors.GREEN)
        config.print_conf()
        raise typer.Exit()

def _notification_test(value: bool) -> None:
    if value:
        Notifier().send('Prova', 'Prova eseguita con successo.')       
        raise typer.Exit()
    
def _init_db(value: bool) -> None:
    if value:
        doc = m.Doc
        raise typer.Exit()

    

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
    check_config: Optional[bool] = typer.Option(
        None,
        "--config",
        "-c",
        help="Check the application's config files.",
        callback=_config_check,
        is_eager=True,
    ),
    notify_test: Optional[bool] = typer.Option(
        None,
        "--notifyTest",
        "-n",
        help="Test Notification.",
        callback=_notification_test,
        is_eager=True,
    ),
    init_db: Optional[bool] = typer.Option(
        None,
        "--initDB",
        "-d",
        help="Init Database.",
        callback=_init_db,
        is_eager=True,
    ),
) -> None:
    return


@app.command()
def importxmldir(
    dir_path: Optional[str] = typer.Option(
        None,
        "--xml_dir_path",
        "-d"
    ),
    verbose: Optional[bool] = typer.Option(
        None,
        "--verbose",
        "-v",
        help="Print the result of command",
    ),
    skip_ct_filter: Optional[bool] = typer.Option(
        False,
        "--skip_ct_filter",
        "-s",
        help="Force reload all dir files",
    ),
) -> None:   
    if dir_path:
        ImportXmlDir().manualImport(dir_path)
    else:  
        ImportXmlDir().autoImportAttive(skip_ct_filter)
        ImportXmlDir().autoImportPassive(skip_ct_filter)
    
    CSVLOGGER.write_csv_rows()
    CSVLOGGER.moveFile()
    input("Press Enter to exit...")
    raise typer.Exit()
