from .default_handler import DefaultHandler
from src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService

class GoogleDorkHandler(DefaultHandler):
    
    
    def handle(self, uri: str):
        if not GoogleDorkCliService().read(uri=uri):
            return super().handle(uri)
        
        return 'No Handler'