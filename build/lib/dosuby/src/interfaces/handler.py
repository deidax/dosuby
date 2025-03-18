from abc import ABC, abstractmethod
from dosuby.src.interfaces.enumeration_handler import EnumerationHandler
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.response.cli.failed_response_builder import FailureResponseBuilder
from dosuby.src.core.domain.cache import Cache


class Handler(EnumerationHandler):
    """
    The Handler interface declares a method for building the chain of subdomain handlers.\n
    It builds a way for creating chained enumerators that enumerat for subdomains is different ways\n
    and return a one final result to the user
    
    """
    
    def __init__(self, next_handler: EnumerationHandler=None) -> None:
        self._next_handler = next_handler
        self.cache = Cache()

    
    def handle(self, uri: str, success_response: SuccessResponse=SuccessResponse()):
        """This method will set the next handler

        Args:
            uri (str): domain target to handle
            success_response (SuccessResponse): success response (will be passed to the next handler)

        Returns:
            Handler: Next handler
        """
        try:
            
            # process to put before the handler
            self.pre_handler_process()
            self._handler_process(uri=uri, success_response=success_response)
            
        except Exception as ex:
            failed_response = FailureResponseBuilder().build_system_error(ex)
            return failed_response.get_response()
            
    
    def run_service(self, uri: str, success_response: SuccessResponse):
        return super().run_service(uri, success_response)

    
    def pre_handler_process(self, **kwargs):
        """This method will be used for specific pre handlers proccessing like displaying a handler name in the console
        """
        pass
    
    
    def _handler_process(self, uri: str, success_response: SuccessResponse):
        self.cache.cached_enumeration_result_count = 0
        service_response = self.run_service(uri=uri, success_response=success_response)
        if type(service_response) is SuccessResponse and self._next_handler:
            return self._next_handler.handle(uri,service_response)
        