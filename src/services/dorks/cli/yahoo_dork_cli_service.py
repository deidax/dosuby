from src.interfaces.subdomain_enumerator_service import SubdomainEnumeratorService
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.yahoo_dorks_adapter import YahooDorksAdapter
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class YahooDorkCliService(SubdomainEnumeratorService):
    
    @classmethod
    def read(cls, uri: str):
        try:
            target_input_dto = TargetInputDTO(uri=uri)
        except InvalidTargetException as ex:
            print(ex)
            return
    
        try:
            
            yahoo_dork = YahooDorksAdapter()
            target_yahoo_dork_usecase = DorksEnumerationUseCase(dork=yahoo_dork)
            result = target_yahoo_dork_usecase.execute(target=target_input_dto)
            for rs in result:
                for r in rs:
                    success_output = SuccessResponseBuilder().set_value(r.get('link'))\
                                                             .set_response_message_and_build('Subdomain Found!')
                    print(success_output.get_response())            
        
        except Exception as ex:
            print(ex)
            return
    
        

    def build_enumerator(self, target_input_dto: TargetInputDTO):
        pass
    

    def process_enumerator(self, result):
        pass       