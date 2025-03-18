from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
import requests
from bs4 import BeautifulSoup
import json

class ThreatMinerAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the ThreatMiner 

        """
        super().__init__()
        self.base_url = "https://api.threatminer.org/v2/domain.php"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    
    @property
    def queries(self):
        """Default ThreatMinerDorkAdapter queries

        Returns:
            list: returns a list of google  queries to enumerate subdomains\n
            for a given target uri
        """
        return {"q": self.target_uri, "rt": "5"}
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new ThreatMiner dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        response = requests.get(url=self.base_url, params=self.queries, headers=self.headers, proxies=None, verify=False)
        if response.status_code == 200:
            try:
                threatminer_json = json.loads(response.text)
                print(threatminer_json)
                for subdomain in threatminer_json:
                    yield subdomain
            except:
                pass
        
        return []
            
        