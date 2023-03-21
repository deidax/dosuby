from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.waybackmachine_enumeration_use_case import WaybackmachineEnumerationUseCase
from src.core.domain.target import Target
from src.adapter.waybackmachine.waybackmachine_adapter import WaybackmachineAdapter
from src.interfaces.success_response import SuccessResponse

from src.interfaces.success_response import SuccessResponse
from src.core.application.strategies.waybackmachine.cli.waybackmachine_cli_enumeration_strategy import WaybackmachineCliEnumerationStrategy

class WaybackmachineCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=WaybackmachineCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        waybackmachine_adapter = WaybackmachineAdapter()
        target_waybackmachine_usecase = WaybackmachineEnumerationUseCase(waybackmachine=waybackmachine_adapter)
        result = target_waybackmachine_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            