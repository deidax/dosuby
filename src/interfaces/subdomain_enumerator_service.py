from abc import ABC, abstractmethod
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException
class SubdomainEnumeratorService(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @classmethod
    def read(cls, uri: str):
        """Read the dorks data to get the domain subdomains using dorks

        Args:
            uri (str): uri target
        """
        print('read')
        try:
            dto = cls()._get_target_method(uri=uri)
        except InvalidTargetException as ex:
            print(ex)
            return False
        
        try:
            result = cls().build_enumerator(target_input_dto=dto)
            
            cls().process_enumerator(result)
        
        except Exception as ex:
            print(ex)
            return False
        
    
    @abstractmethod
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        raise NotImplementedError
    
    @abstractmethod
    def process_enumerator(self, result):
        raise NotImplementedError
                    
    def _get_target_method(self, uri: str) -> TargetInputDTO:
        return TargetInputDTO(uri=uri)
    
    