import requests
import re
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from time import sleep

class BingDorksAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Bing dorks

        """
        super().__init__()
        self.base_url = "https://www.bing.com/search"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    
    @property
    def queries(self):
        """Default BingDorkAdapter queries

        Returns:
            dict: returns a dict of params that will be used to enumerate subdomains\n
            for a given target uri
        """
        return {"q": "domain:." + self.target_uri, "pn": self.target_uri}
    
    def add_dork_queries(self, query: str) -> None:
        """Add a new Bing dork query

        Args:
            query (str): should be a google dork\nex: f'inurl:{target_uri}'

        Returns:
            _type_: None
        """
        return super().add_dork_queries(query)
    

    def _process(self, query):
        # Loop through Bing's search pages, 10 results at a time
        for page in range(1, 200, 10):
            params = self.queries
            params['first'] = str(page)
            response = requests.get(url=self.base_url, headers=self.headers, params=params, proxies=None, verify=False)
            if response.status_code == 200:
                try:
                    if "There are no results for" in response.text:
                        return []
                    else:
                        # Use regex to find all links on the page
                        links = re.findall(r'<a href="(http[s]?://[^"]+)"', response.text)
                        subdomains = [link for link in links if link.startswith("http") and self.target_uri in link]
                        for subdomain in subdomains:
                            yield subdomain
                except:
                    pass
            
            return []
                        