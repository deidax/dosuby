from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
from src.core.domain.target import Target
from src.interfaces.success_response import SuccessResponse
from src.core.application.dorks.cli.default_dork_cli_enumeration_strategy import DefaultDorkCliEnumerationStrategy

class GoogleDorkCliService(SubdomainEnumeratorService):
    
    
    def __init__(self, enumeration_strategy=DefaultDorkCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        google_dork = GoogleDorksAdapter()
        target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)
        result = target_google_dork_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)
                                                            