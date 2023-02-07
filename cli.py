from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler
from src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService


def main():
    
    uri = 'uca.ma'
    
    google = GoogleDorkHandler(uri=uri)
    yahoo = YahooDorkHandler()
    
    google.handle().set_next(handler=yahoo).handle()
    
    # google.handle(uri=uri)
    # yahoo.handle(uri=uri)
    
    # GoogleDorkCliService().read(uri=uri)
    


if __name__ == "__main__":
    main()
