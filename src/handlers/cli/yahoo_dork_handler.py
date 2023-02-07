from .default_handler import DefaultHandler
from src.services.dorks.cli.yahoo_dork_cli_service import YahooDorkCliService

class YahooDorkHandler(DefaultHandler):
    
    
    def handle(self):
        try:
            YahooDorkCliService().read(uri=self._uri)
            return super().handle()
        except Exception as e:
            return e