from abc import ABC, abstractmethod
from dosuby.src.core.application.decorators.loggers_decorators import info_logger

class SubdomainEnumerator(ABC):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using an Adapter (ex: GoogleDorksAdapter) dorks

        """
        super().__init__()
        self._queries = []
        self._target_uri = ''
        self._extra_params = {}
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
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value
    
    
    @abstractmethod
    def add_dork_queries(self, query: str) -> None:
        self.queries.append(query)
    
    # @info_logger("Starting subdomains enumeration...")
    def run(self):
        """This method will run the dork enumeration process

        """
        for query in self.queries:
            yield self._process(query=query)
    
    
    @abstractmethod
    def _process(self, **kwargs):
        """This will run the dork enumeration logic

        Args:
            search_engine (object): search engine to be used
        """
        pass