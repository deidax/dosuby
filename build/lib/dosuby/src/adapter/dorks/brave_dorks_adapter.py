try:
    from dosuby.infrastructure.libs.Search_Engines_Scraper.search_engines import Brave
except ImportError:
    print("No module named 'search_engines' found")
    
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class BraveDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Brave dorks

        """
        super().__init__()
        self.engine = Brave()
    
    @property
    def queries(self):
        """Default BraveDorkAdapter queries

        Returns:
            list: returns a list of Brave dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri} -www.uca.ma',
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Brave dork query

        Args:
            query (str): should be a Brave dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        for page in self.engine.search(query=query,pages=1):
            for p in page:
                yield p
        