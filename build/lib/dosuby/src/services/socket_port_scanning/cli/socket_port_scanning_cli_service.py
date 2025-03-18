from dosuby.src.interfaces.security_enumerator_service import SecurityEnumeratorService
from dosuby.src.core.application.use_cases.ports_enumeration_use_case import PortsEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.ports_scanning.socket_port_scanning_adapter import SocketPortScanningAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.security_enumeration.cli.socket_ports_cli_enumeration_strategy import SocketPortsCliEnumerationStrategy

class SocketPortScanningCliService(SecurityEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=SocketPortsCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target) -> list:
        socket_port_scanning_adapter = SocketPortScanningAdapter()
        socket_port_scanning_usecase = PortsEnumerationUseCase(security_enumerator=socket_port_scanning_adapter)
        result = socket_port_scanning_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(ports=result, success_response=self.success_response)     
                                                            