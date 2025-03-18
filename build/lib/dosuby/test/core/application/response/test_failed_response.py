from dosuby.src.core.application.response.cli.failed_response_builder import FailureResponseBuilder
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

def test_failed_build_invalid_request_exception_object():
    
    ex = InvalidTargetException({'parameter': 'uri', 'message': 'invalid'})
    
    error = FailureResponseBuilder().build_invalid_request_exception_object(ex)
    
    print(error.get_response())