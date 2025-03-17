from abc import ABC, abstractmethod

class SecurityEnumeration(ABC):
    
    def __init__(self) -> None:
        """This class will manage the security enumeration logic

        """
        super().__init__()
        self._target_uri = ''
        self.logger_message = 'SecurityEnumeration'
    
    
    @property
    def target_uri(self):
        return self._target_uri
    
    @target_uri.setter
    def target_uri(self, value):
        self._target_uri = value
        
    
    @abstractmethod
    def run(self):
        """This method will run the security enumeration process

        """
        pass
    
    
    @abstractmethod
    def _process(self, **kwargs):
        """This will run the dork enumeration logic
        """
        pass