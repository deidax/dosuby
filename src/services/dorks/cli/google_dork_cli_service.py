from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class GoogleDorkCliService(SubdomainEnumeratorService):
    
    @classmethod
    def read(cls, uri: str) -> bool:
        try:
            target_input_dto = TargetInputDTO(uri=uri)
        except InvalidTargetException as ex:
            print(ex)
            return False
    
        try:
            
            google_dork = GoogleDorksAdapter()
            target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)
            result = target_google_dork_usecase.execute(target=target_input_dto)
            success_response_builder = SuccessResponseBuilder()
            for rs in result:
                for r in rs:
                    success_output = success_response_builder.set_value(r.get('link'))\
                                                            .set_response_message_and_build('Subdomain Found!')
                    print(success_output.get_response())
            
            print(success_output.get_target_subdomains())
            return True
        
        except Exception as ex:
            print(ex)
            return False       