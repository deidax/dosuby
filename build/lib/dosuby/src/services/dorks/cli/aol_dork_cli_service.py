from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.dorks.aol_dorks_adapter import AolDorksAdapter
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.dorks.cli.default_dork_cli_enumeration_strategy import DefaultDorkCliEnumerationStrategy

class AolDorkCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=DefaultDorkCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        aol_dork = AolDorksAdapter()
        target_aol_dork_usecase = DorksEnumerationUseCase(dork=aol_dork)
        result = target_aol_dork_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            