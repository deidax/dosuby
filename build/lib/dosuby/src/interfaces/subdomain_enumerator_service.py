from abc import ABC, abstractmethod
from dosuby.src.core.domain.target import Target
from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.interfaces.enumeration_strategy import EnumerationStrategy


class SubdomainEnumeratorService(ABC):
    """Abstract class that should be implemented for enumerators services
    """
    
    
    def __init__(self,enumeration_strategy: EnumerationStrategy, success_response: SuccessResponse) -> None:
        """Enumerator service

        Args:
            success_response (SuccessResponse, optional): this attributes will have the service success result. Defaults to SuccessResponse().
        """
        super().__init__()
        self.success_response = success_response
        self.enumeration_strategy = enumeration_strategy
    
    
    def read(self, uri: str):
        """Read the dorks data to get the domain subdomains using dorks
        
        Args:
            uri (str): uri target
        """
        try:
            # probably this should be a singletone
            target = self._get_target_method(uri=uri)
        except InvalidTargetException as ex:
            raise ex
                                    
            # return failed_response
        
        try:
            
            
            self.success_response.set_target(target=target)
            
            result = self.build_enumerator(target=target)
            
            return self.process_enumerator(result)
            
        
        except Exception as ex:
            raise ex
        
    
    @abstractmethod
    def build_enumerator(self, target: Target):
        """This method will build the enumerator to use. example:\n
        google_dork = GoogleDorksAdapter()\n
        target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)\n
        result = target_google_dork_usecase.execute(target=target)\n
        return result\n

        Args:
            target (Target): target to enumerate

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
                    
    def _get_target_method(self, uri: str) -> Target:
        """private method to create a target singleton object

        Args:
            uri (str): domain to enumerate

        Returns:
            Target
        """
        return Target(target_uri=uri, subdomain_serializer=ExtractUriSerializer)
    
    