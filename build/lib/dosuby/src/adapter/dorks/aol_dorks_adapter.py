try:
    from dosuby.infrastructure.libs.Search_Engines_Scraper.search_engines import Aol
except ImportError:
    print("No module named 'search_engines' found")
    
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class AolDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Aol dorks

        """
        super().__init__()
        self.engine = Aol()
    
    @property
    def queries(self):
        """Default AolDorkAdapter queries

        Returns:
            list: returns a list of Aol dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri} -www.uca.ma',
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Aol dork query

        Args:
            query (str): should be a Aol dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        for page in self.engine.search(query=query,pages=1):
            for p in page:
                yield p
        