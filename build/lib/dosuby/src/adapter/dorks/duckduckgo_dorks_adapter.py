try:
    from dosuby.infrastructure.libs.Search_Engines_Scraper.search_engines import Duckduckgo
except ImportError:
    print("No module named 'search_engines' found")
    
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class DuckduckgoDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Duckduckgo dorks

        """
        super().__init__()
        self.engine = Duckduckgo()
    
    @property
    def queries(self):
        """Default DuckduckgoDorkAdapter queries

        Returns:
            list: returns a list of Duckduckgo dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri} -www.{self.target_uri}'
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Duckduckgo dork query

        Args:
            query (str): should be a Bing dork\n'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    
    
    
    def _process(self, query):
        for page in self.engine.search(query=query,pages=40):
            for p in page:
                yield p