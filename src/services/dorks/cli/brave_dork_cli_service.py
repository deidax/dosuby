from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.brave_dorks_adapter import BraveDorksAdapter
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class BraveDorkCliService(SubdomainEnumeratorService):
    
 

    
    
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        brave_dork = BraveDorksAdapter()
        target_brave_dork_usecase = DorksEnumerationUseCase(dork=brave_dork)
        result = target_brave_dork_usecase.execute(target=target_input_dto)
        return result
    
    def process_enumerator(self, result) -> SuccessResponse:
        success_response_builder = SuccessResponseBuilder()
        success_response_builder.success_response = self.success_response
        for rs in result:
            for r in rs:
                if self.success_response.target.add_subdomain(r.get('link')) is True:
                    success_response = success_response_builder.set_response_message_and_build('Subdomain Found!')
                    print(success_response.get_response())
            
        subdomains = success_response.get_target_subdomains()
        print(subdomains)
        
        return success_response     
                                                            