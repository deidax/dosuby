from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from bs4 import BeautifulSoup
import json
import requests

class VirustotalAdapter(SubdomainEnumerator):
    
    def __init__(self) -> None:
        """Manage the enumeration logic using Virustotal

        """
        super().__init__()
        self.base_url = "https://www.virustotal.com/ui/domains/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Ianguage': 'en-US,en;q=0.8', # Ianguage not Language
            'X-Tool': 'vt-ui-main',
            'X-VT-Anti-Abuse-Header': 'purple monkey dishwasher'
        }
    
    @property
    def queries(self):
        """Default VirustotalAdapter queries

        Returns:
            list: returns a list of Virustotal  queries to enumerate subdomains\n
            for a given target uri
        """
        return f"{self.base_url}{self.target_uri}/subdomains?relationships=resolutions"
    
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
        response = requests.get(self.queries, headers=self.headers, proxies=None, verify=False)
        
        if response.status_code == 200:
            try:
                soup = BeautifulSoup(response.text, "lxml")
                virus_total_json = json.loads(soup.text)
                for i in virus_total_json['data']:
                    if i['type'] == 'domain':
                        subdomain = i['id']
                        yield subdomain
                for i in virus_total_json['data']:
                    for domain in i['attributes']['last_https_certificate']['extensions']['subject_alternative_name']:
                        domain = domain.lstrip('*.')
                        yield domain
            except:
                pass
        
        return []
            
        