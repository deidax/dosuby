from .handler_cli import HandlerCli
from src.services.dorks.cli.yahoo_dork_cli_service import YahooDorkCliService
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.failed_response_builder import FailureResponseBuilder


class YahooDorkHandler(HandlerCli):
    
    
    def run_service(self, uri, success_response: SuccessResponse):
        try:
            return YahooDorkCliService(success_response=success_response).read(uri=uri)
        except Exception as ex:
            failed_response = FailureResponseBuilder().build_invalid_request_exception_object(ex)
            print(failed_response) 
    
    
    def __str__(self) -> str:
        return 'Using Yahoo Dork'
    