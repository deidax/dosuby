from dosuby.src.interfaces.security_enumerator_service import SecurityEnumeratorService
from dosuby.src.core.application.use_cases.webserver_enumeration_use_case import WebServerEnumerationUseCase
from dosuby.src.core.domain.subdomain import Subdomain
from dosuby.src.adapter.webserver_scanning.http_client_webserver_scanning_adapter import HttpClientWebserverScanningAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.security_enumeration.cli.webserver_cli_enumeration_strategy import WebserverCliEnumerationStrategy

class WebServerScanningCliService(SecurityEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=WebserverCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Subdomain) -> list:
        http_client_webserver_scanning_adapter = HttpClientWebserverScanningAdapter()
        http_client_webserver_scanning_usecase = WebServerEnumerationUseCase(security_enumerator=http_client_webserver_scanning_adapter)
        result = http_client_webserver_scanning_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(webserver=result, success_response=self.success_response)     
                                                            