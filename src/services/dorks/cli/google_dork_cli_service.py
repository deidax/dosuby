from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
from src.interfaces.success_response import SuccessResponse


from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class GoogleDorkCliService(SubdomainEnumeratorService):
    
 

    
    
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        google_dork = GoogleDorksAdapter()
        target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)
        result = target_google_dork_usecase.execute(target=target_input_dto)
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
            
        # print(success_output.get_target_subdomains())
                                                            