from dosuby.src.interfaces.response_builder import ResponseBuilder
from dosuby.src.interfaces.failed_response import FailedResponse
from dosuby.src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

class FailureResponseBuilder(ResponseBuilder):

    def __init__(self) -> None:
        """
        A builder instance should contain a blank response object
        which is used in further assembly
        """
        self._failure_response = FailedResponse()
    
    def set_value(self, value):
        self._failure_response.response_value = value
        return self
    
    def set_type(self, value=None):
        self._failure_response.response_type = value
        return self
    
    def default_type(self):
        self._failure_response.response_type = CliResponseTypeEnums.ERROR
        return self
    
    def set_response_message(self, message_value):
        self._failure_response.response_message = message_value
        return self

    def build_response(self):
        self._failure_response.response_value = {
            'type': self._failure_response.response_type,
            'cause':  self._failure_response.cause_of_failure,
            'message': self._failure_response.response_message
        }
        
        
        return self._failure_response
    
    def _set_status_code(self, response_failed_type):
        self._failure_response.status_code = response_failed_type['status_code']
        return self
    
    def set_response_message_and_build(self, message_value=''):
        failure_builder = self.default_type().set_response_message(message_value)
        return failure_builder.build_response()
    
    def _set_cause_of_failure(self, value=CliResponseTypeEnums.PARAMETERS_ERROR):
        self._failure_response.cause_of_failure = value
        self = self._set_status_code(value)
        return self
        
    def build_invalid_request_exception_object(self, exc: InvalidTargetException):
        #default value 'PARAMETERS_ERROR'
        failure_response = self._set_cause_of_failure()\
                              .set_response_message_and_build(exc)
                             
        return failure_response

    def build_resource_error(self, message_value=''):
        failure_response = self._set_cause_of_failure(value=CliResponseTypeEnums.RESOURCE_ERROR)\
                              .set_response_message_and_build(message_value)
        
        return failure_response
    
    def build_parameters_error(self, message_value=''):
        failure_response = self._set_cause_of_failure()\
                            .set_response_message_and_build(message_value)
    
        return failure_response

    def build_system_error(self, message_value=''):
        RESP_TYPE = CliResponseTypeEnums.SYSTEM_ERROR
        failure_response = self._set_cause_of_failure(value=RESP_TYPE)\
                            ._set_status_code(response_failed_type=RESP_TYPE)\
                            .set_response_message_and_build(message_value)

        return failure_response