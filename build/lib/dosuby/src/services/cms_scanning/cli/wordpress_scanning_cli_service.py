from dosuby.src.interfaces.security_enumerator_service import SecurityEnumeratorService
from dosuby.src.core.application.use_cases.cms_enumeration_use_case import CMSEnumerationUseCase
from dosuby.src.core.domain.subdomain import Subdomain
from dosuby.src.adapter.cms_scanning.wordpress_scanning_adapter import WordPressScanningAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.security_enumeration.cli.cms_cli_enumeration_strategy import CMSCliEnumerationStrategy

class WordPressScanningCliService(SecurityEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=CMSCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Subdomain) -> list:
        cms_scanning_adapter = WordPressScanningAdapter()
        cms_scanning_usecase = CMSEnumerationUseCase(security_enumerator=cms_scanning_adapter)
        result = cms_scanning_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(cms=result, success_response=self.success_response)     
                                                            