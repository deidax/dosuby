from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.alientvault_enumeration_use_case import AlientvaultEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.alientvault.alientvault_adapter import AlientvaultAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.alientvault.cli.alientvault_cli_enumeration_strategy import AlientvaultCliEnumerationStrategy

class AlientvaultCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=AlientvaultCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        alientvault_adapter = AlientvaultAdapter()
        target_alientvault_usecase = AlientvaultEnumerationUseCase(alientvault=alientvault_adapter)
        result = target_alientvault_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            