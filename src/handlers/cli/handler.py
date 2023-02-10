from abc import ABC, abstractmethod
from src.interfaces.enumeration_handler import EnumerationHandler
from src.interfaces.success_response import SuccessResponse

class Handler(EnumerationHandler):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.\n
    It builds a way for creating chained enumerators that enumerat for subdomains is different ways\n
    and return a one final result to the user
    
    """

    def __init__(self, next_handler: EnumerationHandler=None) -> None:
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, uri: str, success_response: SuccessResponse):
        """This method will set the next handler

        Args:
            uri (str): domain target to handle
            success_response (SuccessResponse): success response (will be passed to the next handler)

        Returns:
            Handler: Next handler
        """
        if self._next_handler:
            return self._next_handler.handle(uri,success_response)
        
        return