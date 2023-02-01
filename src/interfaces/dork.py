from abc import ABC, abstractmethod

class Dork(ABC):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using an Adapter (ex: GoogleDorksAdapter) dorks

        """
        super().__init__()
        self._queries = []
        self._target_uri = ''
        self._extra_params = {}
        self._subdomains = []
    
    
    @property
    def target_uri(self):
        return self._target_uri
    
    @target_uri.setter
    def target_uri(self, value):
        self._target_uri = value
        
    @property
    def queries(self):
        return self._queries
    
    @queries.setter
    def queries(self, value):
        pass
    
    @property
    def subdomains(self):
        return self._subdomains
    
    @subdomains.setter
    def subdomains(self, value):
        self._subdomains.append(value)
    
    
    @abstractmethod
    def add_dork_queries(self, query: str) -> None:
        self.queries.append(query)
    
    @abstractmethod
    def run(self):
        """This method will run the dork enumeration logic

        Returns:
            None
        """
    
    @abstractmethod
    def get_results(self) -> dict:
        """Get the result output of the enumerated subdomains

        Returns:
            dict: dictionary output of enumerated subdomains
        """
        return self.subdomains