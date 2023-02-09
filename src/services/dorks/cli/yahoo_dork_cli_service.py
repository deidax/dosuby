from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.yahoo_dorks_adapter import YahooDorksAdapter
from src.interfaces.success_response import SuccessResponse

from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class YahooDorkCliService(SubdomainEnumeratorService):
    
    
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        yahoo_dork = YahooDorksAdapter()
        target_yahoo_dork_usecase = DorksEnumerationUseCase(dork=yahoo_dork)
        result = target_yahoo_dork_usecase.execute(target=target_input_dto)
        return result
    
    def process_enumerator(self, result):
        success_response = SuccessResponse()
        success_response_builder = SuccessResponseBuilder()
        success_response_builder.success_response = success_response
        for rs in result:
            for r in rs:
                if success_response.target.add_subdomain(r.get('link')) is True:
                    success_output = success_response_builder.set_response_message_and_build('Subdomain Found!')
                    print(success_output.get_response())
        
        subdomains = success_output.get_target_subdomains()
        print(subdomains)
        
        return subdomains     