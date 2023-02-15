from src.interfaces.enumeration_strategy import EnumerationStrategy
from src.interfaces.success_response import SuccessResponse
from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

class SocketPortsCliEnumerationStrategy(EnumerationStrategy):
    
    
    def enumeration_process(self, **kwargs) -> list:
        """_summary_

        Args:
            result(generator): result  to process
            success_response (SuccessResponse): this will be used to get the final success response
        Returns:
            list: results list
        """
        # success_response = kwargs.get('success_response')
        # success_response_builder = SuccessResponseBuilder()
        # success_response_builder.success_response = success_response
        # # success response for each handler
        # tmp_success_response = SuccessResponse()
        # for row in rows:
        #     for cell in row:
        #         if len(cell) >= 5:
        #             sub = cell[4]
        #             if success_response.target.add_subdomain(sub.text) is True:
        #                 tmp_success_response = success_response_builder.set_response_message_and_build('Subdomain Found!')
        #                 print(tmp_success_response.get_response())
            
        # subdomains = tmp_success_response.get_target_subdomains()
        # print(subdomains)
        
        # return tmp_success_response