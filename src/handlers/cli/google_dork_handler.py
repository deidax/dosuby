from .handler import Handler
from src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService

class GoogleDorkHandler(Handler):
    
    
    def handle(self, uri):
        try:
            GoogleDorkCliService().read(uri=uri)
            return super().handle(uri)
        except Exception as e:
            return e
            