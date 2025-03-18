try:
    from dosuby.infrastructure.libs.Search_Engines_Scraper.search_engines import Google
except ImportError:
    print("No module named 'search_engines' found")
    
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class GoogleDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Google dorks

        """
        super().__init__()
        self.engine = Google()
    
    @property
    def queries(self):
        """Default GoogleDorkAdapter queries

        Returns:
            list: returns a list of google dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri} -www',
            f'site:{self.target_uri} -www',
            f'site:*.{self.target_uri}  -www',
            f'site:*.*.{self.target_uri}  -www',
            f'site:*.*.*{self.target_uri}  -www',
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Google dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        for page in self.engine.search(query=query,pages=1):
            for p in page:
                yield p
        