from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
import requests

class HackertargetAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """Manage the enumeration logic using Hackertarget

        """
        super().__init__()
        self.base_url = "https://api.hackertarget.com/hostsearch/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    
    @property
    def queries(self):
        """Default HackertargetAdapter queries

        Returns:
            list: returns a list of Hackertarget  queries to enumerate subdomains\n
            for a given target uri
        """
        return {"q": self.target_uri}
    
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
        response = requests.get(self.base_url, headers=self.headers, params=self.queries)
        if response.status_code == 200:
            try:
                line = response.text.split('\n')
                # Find the <pre> tag
                for l in line:
                    subdomain = l.split(',')[0]
                    yield subdomain
            except:
                pass
        
        return []
            
        