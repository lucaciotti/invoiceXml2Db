from src.provider.csvLogger import csvLogger
from src import cli, __app_name__

CSVLOGGER = csvLogger()

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()