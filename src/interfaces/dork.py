from abc import ABC, abstractmethod

class Dork(ABC):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using an Adapter (ex: GoogleDorksAdapter) dorks

        """
        super().__init__()
        self._querys = []
        self._target_uri = ''
        self._extra_params = {}
    
    
    @property
    def target_uri(self):
        return self._target_uri
    
    @target_uri.setter
    def target_uri(self, value):
        self._target_uri = value
    
    
    @abstractmethod
    def _set_dork_queries(self, query: str):
        pass
    
    @abstractmethod
    def get_results(self) -> dict:
        """Get the result output of the enumerated subdomains

        Returns:
            dict: dictionary output of enumerated subdomains
        """
        return ['fake.sometext.test', 'dork.sometext.test']