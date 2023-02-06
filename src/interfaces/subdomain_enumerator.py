from abc import ABC, abstractmethod
from src.core.domain.target import Target

class SubdomainEnumerator(ABC):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using an Adapter (ex: GoogleDorksAdapter) dorks

        """
        super().__init__()
        self._queries = []
        self._target_uri = ''
        self._extra_params = {}
        self._target = Target()
        self._engine = None
    
    
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
        return self._target
    
    @subdomains.setter
    def subdomains(self, value):
        self._target.append(value)
    
    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value
    
    
    @abstractmethod
    def add_dork_queries(self, query: str) -> None:
        self.queries.append(query)
    
    def run(self):
        """This method will run the dork enumeration process

        """
        for query in self.queries:
            yield self._process(query=query)
    
    @abstractmethod
    def get_results(self) -> list:
        """Get the result output of the enumerated subdomains

        Returns:
            dict: dictionary output of enumerated subdomains
        """
        return self.subdomains
    
    @abstractmethod
    def _process(self, query):
        """This will run the dork enumeration logic

        Args:
            search_engine (object): search engine to be used
        """
        pass