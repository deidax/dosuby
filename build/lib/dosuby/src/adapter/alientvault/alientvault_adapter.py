from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
import requests
from bs4 import BeautifulSoup
import json

class AlientvaultAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """Manage the enumeration logic using Alientvault

        """
        super().__init__()
        self.base_url = "https://otx.alienvault.com/api/v1/indicators/domain/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    
    @property
    def queries(self):
        """Default AlientvaultAdapter queries

        Returns:
            list: returns a list of Alientvault  queries to enumerate subdomains\n
            for a given target uri
        """
        return [
            f'{self.base_url}{self.target_uri}/passive_dns'
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
        response = requests.get(query, headers=self.headers, proxies=None, verify=False)
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, 'lxml')
                # Find the <pre> tag
                alienvault_json = json.loads(soup.text)
                for subdomain in alienvault_json['passive_dns']:
                    yield subdomain['hostname']
            except:
                pass
        
        return []
            
        