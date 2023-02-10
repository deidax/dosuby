from abc import ABC, abstractmethod
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.failed_response_builder import FailureResponseBuilder

class SubdomainEnumeratorService(ABC):
    """Abstract class that should be implemented for enumerators services
    """
    
    def __init__(self, success_response: SuccessResponse=SuccessResponse()) -> None:
        """Enumerator service

        Args:
            success_response (SuccessResponse, optional): this attributes will have the service success result. Defaults to SuccessResponse().
        """
        super().__init__()
        self.success_response = success_response
    
    @classmethod
    def read(cls, uri: str):
        """Read the dorks data to get the domain subdomains using dorks

        Args:
            uri (str): uri target
        """
        try:
            dto = cls()._get_target_method(uri=uri)
        except InvalidTargetException as ex:
            raise ex
                                    
            # return failed_response
        
        try:
            result = cls().build_enumerator(target_input_dto=dto)
            
            return cls().process_enumerator(result)
            
        
        except Exception as ex:
            raise ex
        
    
    @abstractmethod
    def build_enumerator(self, target_input_dto: TargetInputDTO):
        """This method will build the enumerator to use. example:\n
        google_dork = GoogleDorksAdapter()\n
        target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)\n
        result = target_google_dork_usecase.execute(target=target_input_dto)\n
        return result\n

        Args:
            target_input_dto (TargetInputDTO): target input dto that will validate the user input

        Raises:
            NotImplementedError: This method should be used for any enumerator service
        """
        raise NotImplementedError
    
    @abstractmethod
    def process_enumerator(self, result) -> SuccessResponse:
        """This method will hold the logic of enumeration process for each service\n
        this method should use the self.success_response and return it after the process is over.

        Args:
            result (Generator): the result should be a generator

        Raises:
            NotImplementedError: This method should be used for any enumerator service
        """
        raise NotImplementedError
                    
    def _get_target_method(self, uri: str) -> TargetInputDTO:
        """private method to create a target DTO object

        Args:
            uri (str): domain to enumerate

        Returns:
            TargetInputDTO
        """
        return TargetInputDTO(uri=uri)
    
    