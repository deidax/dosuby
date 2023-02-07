from .default_handler import DefaultHandler
from src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService

class GoogleDorkHandler(DefaultHandler):
    
    
    def handle(self):
        try:
            GoogleDorkCliService().read(uri=self._uri)
            return self
        except Exception as e:
            return e
            