from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.yoga_enumeration_use_case import YogaEnumerationUseCase
from src.core.domain.target import Target
from src.adapter.yoga.yoga_adapter import YogaAdapter
from src.interfaces.success_response import SuccessResponse

from src.interfaces.success_response import SuccessResponse
from src.core.application.strategies.yoga.cli.yoga_cli_enumeration_strategy import YogaCliEnumerationStrategy

class YogaCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=YogaCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        yoga_adapter = YogaAdapter()
        target_yoga_usecase = YogaEnumerationUseCase(yoga=yoga_adapter)
        result = target_yoga_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            