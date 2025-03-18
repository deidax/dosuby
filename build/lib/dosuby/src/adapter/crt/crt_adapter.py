try:
    from dosuby.infrastructure.libs.CrtSearch.crt_search import CrtSearch
except ImportError:
    print("No module named 'search_engines' found")
    
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class CrtAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the CrtSearch

        """
        super().__init__()
        self.engine = CrtSearch()
    
    @property
    def queries(self):
        """Default CrtAdapter queries

        Returns:
            list: returns a list of CrtSearch queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'{self.target_uri}'
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new CrtSeach query
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        for page in self.engine.search(query=query):
            yield page.find_all("td")
        