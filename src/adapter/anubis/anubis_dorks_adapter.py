from src.interfaces.subdomain_enumerator import SubdomainEnumerator
import requests
from bs4 import BeautifulSoup
import json

class AnubisAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Anubis 

        """
        super().__init__()
        self.base_url = "https://jonlu.ca/anubis/subdomains/"
    
    @property
    def queries(self):
        """Default AnubisDorkAdapter queries

        Returns:
            list: returns a list of google  queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'{self.base_url}{self.target_uri}'
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
        response = requests.get(query, proxies=None, verify=False)
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find the <pre> tag
                anubis_json = json.loads(response.text)
                for subdomain in anubis_json:
                    yield subdomain
            except:
                pass
        
        return []
            
        