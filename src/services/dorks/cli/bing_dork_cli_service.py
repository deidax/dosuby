from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.adapter.dorks.bing_dorks_adapter import BingDorksAdapter
from src.core.domain.target import Target
from src.interfaces.success_response import SuccessResponse
from src.core.application.dorks.cli.bing_dork_cli_enumeration_strategy import BingDorkCliEnumerationStrategy
from src.core.application.dorks.cli.default_dork_cli_enumeration_strategy import DefaultDorkCliEnumerationStrategy


class BingDorkCliService(SubdomainEnumeratorService):
    
    
    def __init__(self, enumeration_strategy=BingDorkCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        bing_dork = BingDorksAdapter()
        target_bing_dork_usecase = DorksEnumerationUseCase(dork=bing_dork)
        result = target_bing_dork_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)
                                                            