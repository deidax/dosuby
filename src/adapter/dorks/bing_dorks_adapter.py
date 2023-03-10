try:
    from infrastructure.libs.Search_Engines_Scraper.search_engines import Bing
except ImportError:
    print("No module named 'search_engines' found")
    
from src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class BingDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Bing dorks

        """
        super().__init__()
        self.engine = Bing()
    
    @property
    def queries(self):
        """Default BingDorkAdapter queries

        Returns:
            list: returns a list of bing dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'domain:{self.target_uri}'
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Bing dork query

        Args:
            query (str): should be a bing dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        for page in self.engine.search(query=query,pages=1):
            for p in page:
                print(next(p))
                yield p
        