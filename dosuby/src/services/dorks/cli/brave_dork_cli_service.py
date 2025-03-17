from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.domain.target import Target
from src.adapter.dorks.brave_dorks_adapter import BraveDorksAdapter
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder
from src.interfaces.success_response import SuccessResponse
from src.core.application.strategies.dorks.cli.default_dork_cli_enumeration_strategy import DefaultDorkCliEnumerationStrategy

class BraveDorkCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=DefaultDorkCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        brave_dork = BraveDorksAdapter()
        target_brave_dork_usecase = DorksEnumerationUseCase(dork=brave_dork)
        result = target_brave_dork_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            