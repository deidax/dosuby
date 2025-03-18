import requests
import re
from bs4 import BeautifulSoup
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class AskDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Ask dorks

        """
        super().__init__()
        self.base_url = "https://www.ask.com/web"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    
    @property
    def queries(self):
        """Default AskDorkAdapter queries

        Returns:
            dict: returns a dict of params that will be used to enumerate subdomains\n
            for a given target uri
        """
        return {"q": self.target_uri}
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Ask dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        # Loop through Ask's search pages, 10 results at a time
        for page in range(1, 5):
            params = self.queries
            params['page'] = str(page)
            response = requests.get(url=self.base_url, headers=self.headers, params=params, proxies=None, verify=False)
            if response.status_code == 200:
                try:
                    soup = BeautifulSoup(response.text, "html.parser")
                    links = soup.findAll("a")
                    for link in links:
                        subdomain = link.get("href")
                        yield subdomain
                except:
                    pass
            
            return []
                        