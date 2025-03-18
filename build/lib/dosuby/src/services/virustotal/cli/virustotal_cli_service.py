from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.virustotal_enumeration_use_case import VirustotalEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.virustotal.virustotal_adapter import VirustotalAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.virustotal.cli.virustotal_cli_enumeration_strategy import VirustotalCliEnumerationStrategy

class VirustotalCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=VirustotalCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        virustotal_adapter = VirustotalAdapter()
        target_virustotal_usecase = VirustotalEnumerationUseCase(virustotal=virustotal_adapter)
        result = target_virustotal_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            