from abc import ABC, abstractmethod
from dosuby.src.core.application.enums.cli_response_type_enum import CliResponseTypeEnums

class ResponseBuilder(ABC):
    """
    This is a builder interface to specifie methods for creating
    the different parts of the Response object
    """
    
    @staticmethod
    @abstractmethod
    def set_type(value=None):
        pass
    
    @staticmethod
    @abstractmethod
    def set_value(value=None):
        pass
    
        
    @staticmethod
    @abstractmethod
    def set_response_message(message_value=''):
        pass
    
    @staticmethod
    @abstractmethod
    def build_response():
        pass
    
    @staticmethod
    @abstractmethod
    def set_response_message_and_build(message_value=''):
        pass
    
    @staticmethod
    @abstractmethod
    def _set_status_code(resp_type: CliResponseTypeEnums):
        pass