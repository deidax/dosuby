from dosuby.src.interfaces.enumeration_strategy import EnumerationStrategy
from dosuby.src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class SocketPortsCliEnumerationStrategy(EnumerationStrategy):
    
    
    def enumeration_process(self, **kwargs) -> list:
        """_summary_

        Args:
            result(generator): result  to process
            success_response (SuccessResponse): this will be used to get the final success response
        Returns:
            list: results list
        """
        # success response for each handler
        ports = kwargs.get('ports')
       
        if ports:
            return ports
        return []