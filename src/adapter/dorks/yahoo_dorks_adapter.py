try:
    from infrastructure.libs.Search_Engines_Scraper.search_engines import Yahoo
except ImportError:
    print("No module named 'search_engines' found")
    
from src.interfaces.dork import Dork
from time import sleep

class YahooDorksAdapter(Dork):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Yahoo dorks

        """
        super().__init__()
    
    @property
    def queries(self):
        """Default YahooDorkAdapter queries

        Returns:
            list: returns a list of Yahoo dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri}'
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Yahoo dork query

        Args:
            query (str): should be a Yahoo dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    
    def get_results(self) -> dict:
        return super().get_results()
    
    def run(self):
        yahoo = Yahoo()
        for query in self.queries:
            for page in yahoo.search(query=query,pages=10):
                yield page
                # for result in q:
                #     self.subdomains = result.get('link')
                #     print(result.get('link')
            
            sleep(2)
        
        # return self.get_results()