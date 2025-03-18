from dosuby.src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from dosuby.src.core.application.use_cases.threatminer_enumeration_use_case import ThreatMinerEnumerationUseCase
from dosuby.src.core.domain.target import Target
from dosuby.src.adapter.threatminer.threatminer_adapter import ThreatMinerAdapter
from dosuby.src.interfaces.success_response import SuccessResponse

from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.strategies.threatminer.cli.threathminer_search_cli_enumeration_strategy import ThreatMinerCliEnumerationStrategy

class ThreatMinerCliService(SubdomainEnumeratorService):
    
 
    def __init__(self, enumeration_strategy=ThreatMinerCliEnumerationStrategy(), success_response=SuccessResponse()) -> None:
        super().__init__(enumeration_strategy, success_response)
    
    
    def build_enumerator(self, target: Target):
        threatminer = ThreatMinerAdapter()
        target_threatminer_usecase = ThreatMinerEnumerationUseCase(dork=threatminer)
        result = target_threatminer_usecase.execute(target=target)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        return self.enumeration_strategy.enumeration_process(subdomains_links=result, success_response=self.success_response)     
                                                            