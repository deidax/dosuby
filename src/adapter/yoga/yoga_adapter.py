from src.interfaces.subdomain_enumerator import SubdomainEnumerator

class YogaAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """Manage the enumeration logic using Yoga

        """
        super().__init__()
    
    @property
    def queries(self):
        """Default YogaAdapter queries

        Returns:
            list: returns a list of Yoga  queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            
        ]
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Anubis dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        # write your process logic here
        pass
            
        