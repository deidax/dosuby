from abc import ABC, abstractmethod
from dosuby.src.interfaces.success_response import SuccessResponse

class EnumerationHandler(ABC):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.
    """


    @abstractmethod
    def handle(self, uri: str, success_response: SuccessResponse=SuccessResponse()):
        pass
    
    @abstractmethod
    def run_service(self, uri: str, success_response: SuccessResponse):
        """This method will run the enumerator service for each service handler

        Args:
            success_response (SuccessResponse): success response (will be passed to the next handler)

        Raises:
            NotImplementedError: Method should be implemented by all Handlers
        """
        raise NotImplementedError
