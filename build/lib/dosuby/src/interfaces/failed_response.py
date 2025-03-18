import sys, os
from .search_response import SearchResponse
from dosuby.src.core.domain.target import Target

class FailedResponse(SearchResponse):
    def __init__(self) -> None:
        super().__init__()
        self._res_cause_of_failure = None
    
    @property
    def cause_of_failure(self):
        if self._res_cause_of_failure is None: return 'Unknown'
        if self._res_cause_of_failure['label'] is None: return 'Unkonwn'
        return self._res_cause_of_failure['label']
    
    @property
    def cause_of_failure_to_dict(self):
        return self._res_cause_of_failure
    
    @cause_of_failure.setter
    def cause_of_failure(self, value):
        self._res_cause_of_failure = value
        
    @property
    def response_type_to_dict(self):
        return self._res_type
    
    
    def _format_message(self, msg):
        if isinstance(msg, Exception):
            exc_type, exc_obj, exc_tb = sys.exc_info()
            if exc_tb is not None:
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                line_number = exc_tb.tb_lineno
                return "{}: {} in '{}' line {}".format(msg.__class__.__name__, "{}".format(msg), "{}".format(fname), "{}".format(line_number))
           
            return "{}: {} ".format(msg.__class__.__name__, "{}".format(msg))

        return msg

    
    def get_response(self):
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'cause': self.cause_of_failure,
            'message': self._format_message(self.response_message),
        }
        
        return  f"Status:   {response.get('status_code')}\n"\
                f"{'-'*10}\n"\
                f"Type:     {response.get('type')}\n"\
                f"Message:  '{response.get('message')}'\n"\
                f"{'-'*10}\n"

    def __str__(self) -> str:
        return self.get_response()
    
    def set_target(self, target: Target):
        return super().set_target(target)