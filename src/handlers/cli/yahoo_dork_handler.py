from .handler import Handler
from src.services.dorks.cli.yahoo_dork_cli_service import YahooDorkCliService
from src.interfaces.success_response import SuccessResponse

class YahooDorkHandler(Handler):
    
    
    def handle(self, uri, success_response: SuccessResponse=SuccessResponse()):
        try:
            YahooDorkCliService(success_response=success_response).read(uri=uri)
            return super().handle(uri, success_response)
        except Exception as e:
            return e