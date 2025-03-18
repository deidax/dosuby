from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.hackertarget_enumeration_use_case import HackertargetEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.hackertarget.hackertarget_adapter import HackertargetAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.hackertarget.cli.hackertarget_cli_enumeration_strategy import HackertargetCliEnumerationStrategy

class HackertargetCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=HackertargetCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        hackertarget_adapter = HackertargetAdapter()
        target_hackertarget_usecase = HackertargetEnumerationUseCase(hackertarget=hackertarget_adapter)
        result = target_hackertarget_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            