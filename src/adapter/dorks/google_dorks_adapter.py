from src.interfaces.dork import Dork

class GoogleDorksAdapter(Dork):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Google dorks

        """
        super().__init__()
    
    @property
    def queries(self):
        """Default GoogleDorkAdapter queries

        Returns:
            list: returns a list of google dorks queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'site:{self.target_uri} -www',
            f'site:*.{self.target_uri}',
            f'inurl:{self.target_uri}',
            f'inurl:{self.target_uri} -www'
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Google dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    
    def get_results(self) -> dict:
        return super().get_results()
    
    def run(self):
        pass