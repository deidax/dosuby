from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.crt_enumeration_use_case import CrtEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.crt.crt_adapter import CrtAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.crt.cli.crt_search_cli_enumeration_strategy import CrtSearchCliEnumerationStrategy

class CrtCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=CrtSearchCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        crt_adapter = CrtAdapter()
        target_crt_usecase = CrtEnumerationUseCase(crt=crt_adapter)
        result = target_crt_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(rows=result, success_response=self.success_response)     
                                                            