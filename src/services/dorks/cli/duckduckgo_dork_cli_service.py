from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.duckduckgo_dorks_adapter import DuckduckgoDorksAdapter

from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class DuckduckgoDorkCliService(SubdomainEnumeratorService):
    
    
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        duckduckgo_dork = DuckduckgoDorksAdapter()
        target_Duckduckgo_dork_usecase = DorksEnumerationUseCase(dork=duckduckgo_dork)
        result = target_Duckduckgo_dork_usecase.execute(target=target_input_dto)
        return result
    
    def process_enumerator(self, result):
        success_response_builder = SuccessResponseBuilder()
        success_response_builder.success_response = self.success_response
        for rs in result:
            for r in rs:
                if self.success_response.target.add_subdomain(r.get('link')) is True:
                    success_output = success_response_builder.set_response_message_and_build('Subdomain Found!')
                    print(success_output.get_response())
        
        subdomains = success_output.get_target_subdomains()
        print(subdomains)
        
        return success_output     