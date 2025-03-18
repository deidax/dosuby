from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.anubis_enumeration_use_case import AnubisEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.anubis.anubis_dorks_adapter import AnubisAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.anubis.cli.anubis_search_cli_enumeration_strategy import AnubisCliEnumerationStrategy

class AnubisCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=AnubisCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        anubis = AnubisAdapter()
        target_anubis_usecase = AnubisEnumerationUseCase(dork=anubis)
        result = target_anubis_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            