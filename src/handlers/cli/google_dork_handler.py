from .handler import Handler
from src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService
from src.interfaces.success_response import SuccessResponse

class GoogleDorkHandler(Handler):
    
    
    def handle(self, uri, success_response: SuccessResponse=SuccessResponse()):
        try:
            GoogleDorkCliService(success_response=success_response).read(uri=uri)
            return super().handle(uri,success_response)
        except Exception as e:
            return e
            