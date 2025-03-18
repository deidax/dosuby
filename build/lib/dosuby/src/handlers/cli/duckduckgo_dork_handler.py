from .handler_cli import HandlerCli
from dosuby.src.services.dorks.cli.duckduckgo_dork_cli_service import DuckduckgoDorkCliService
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.response.cli.failed_response_builder import FailureResponseBuilder

class DuckduckgoDorkHandler(HandlerCli):
    
    
    def run_service(self, uri, success_response: SuccessResponse):
        try:
            return DuckduckgoDorkCliService(success_response=success_response).read(uri=uri)
        except Exception as ex:
            failed_response = FailureResponseBuilder().build_invalid_request_exception_object(ex)
            print(failed_response) 
    
    def __str__(self) -> str:
        return 'Using Duckduckgo Dork'
        
            