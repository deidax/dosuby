from src.interfaces.response_builder import ResponseBuilder
from src.interfaces.success_response import SuccessResponse
from src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums

class SuccessResponseBuilder(ResponseBuilder):

    def __init__(self) -> None:
        """
        A builder instance should contain a blank response object
        which is used in further assembly
        """
        self._success_response = SuccessResponse()
        self._success_response.status_code = CliResponseTypeEnums.SUCCESS['status_code']
        self._success_response._res_type = CliResponseTypeEnums.SUCCESS
    
    def set_type(self, value):
        """Success Response is set by default"""
        pass
    
    def set_value(self, value):
        self._success_response.response_value = value
        self._success_response.target.subdomain = value
        return self
    
    def set_response_message(self, message_value):
        self._success_response.response_message = message_value
        return self
    
    def build_response(self):
        return self._success_response
    
    def set_response_message_and_build(self, message_value):
        success_builder = self.set_response_message(message_value)
        return success_builder.build_response()
    
    def _set_status_code(resp_type: CliResponseTypeEnums):
        """Status code is set by default for Success Response"""
        pass