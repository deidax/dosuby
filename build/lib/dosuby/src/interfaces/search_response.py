from abc import ABC, abstractmethod
from dosuby.src.core.domain.target import Target
from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer


class SearchResponse(ABC):
    
    def __init__(self) -> None:
        """This abstract class manages the search response
        """
        self._res_type = None
        self._res_value = None
        self._target = None
        self._res_message = ''
        self._status_code = None
    
    @property
    def response_value(self):
        return self._res_value
    
    @response_value.setter
    def response_value(self, value):
        self._res_value = value
    
    @property
    def response_type(self):
        return self._res_type['label']
    
    @response_type.setter
    def response_type(self, value):
        self._res_type = value
        
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, value):
        self._target.add_subdomain(value)
    
    @property
    def response_message(self):
        return self._res_message
    
    @response_message.setter
    def response_message(self, value):
        self._res_message = value
    
    @property
    def status_code(self):
        return self._status_code
    @status_code.setter
    def status_code(self, value):
        self._status_code = value
    
    
    def __bool__(self):
        return self._res_type['value']
    
    @abstractmethod
    def get_response(self):
        """Return search results
        """
        pass
    
    @abstractmethod
    def set_target(self, target: Target):
        self._target = target