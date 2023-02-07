from .search_response import SearchResponse

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
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    
    def get_response(self):
        response = {
            'type': self.response_type,
            'status_code': self.status_code,
            'cause': self.cause_of_failure,
            'message': self.response_message,
        }
        
        return  f"Status:    {response.get('status_code')}\n"\
                f"Type:    {response.get('type')}\n"\
                f"Message:   {response.get('message')}\n"\
                f"Cause: {response.get('cause')}\n"\
                f"{'-'*10}\n"
