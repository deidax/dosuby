from abc import ABC, abstractmethod
from src.core.domain.target import Target

class SecurityEnumeration(ABC):
    
    def __init__(self) -> None:
        """This class will manage the security enumeration logic

        """
        super().__init__()
        self._target_uri = ''
        self.engine = None
    
    @property
    def target_uri(self):
        return self._target_uri
    
    @target_uri.setter
    def target_uri(self, value):
        self._target_uri = value
        
    
    def run(self):
        """This method will run the dork enumeration process

        """
        for query in self.queries:
            yield self._process(query=query)
    
    
    @abstractmethod
    def _process(self, **kwargs):
        """This will run the dork enumeration logic
        """
        pass