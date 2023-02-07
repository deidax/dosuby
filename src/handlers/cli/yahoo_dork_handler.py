from .default_handler import DefaultHandler
from src.services.dorks.cli.yahoo_dork_cli_service import YahooDorkCliService

class YahooDorkHandler(DefaultHandler):
    
    
    def handle(self, uri: str):
        try:
            YahooDorkCliService().read(uri=uri)
            return super().handle(uri)
        except Exception as e:
            return e