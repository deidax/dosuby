from .handler import Handler
from src.services.dorks.cli.yahoo_dork_cli_service import YahooDorkCliService

class YahooDorkHandler(Handler):
    
    
    def handle(self, uri):
        try:
            YahooDorkCliService().read(uri=uri)
            return super().handle(uri)
        except Exception as e:
            return e