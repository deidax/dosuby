from dosuby.src.interfaces.enumeration_strategy import EnumerationStrategy

class WebserverCliEnumerationStrategy(EnumerationStrategy):
    
    
    def enumeration_process(self, **kwargs):
        """_summary_

        Args:
            result(Any): result  to process
            success_response (SuccessResponse): this will be used to get the final success response
        Returns:
            list: results list
        """
        # success response for each handler
        webserver = kwargs.get('webserver')
       
        return webserver