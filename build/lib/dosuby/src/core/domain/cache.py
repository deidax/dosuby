from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton

@dataclass
class Cache(metaclass=Singleton):
    """Cache ips to use in real time execution
    """
    
    #this will be used for display
    tmp_subdomains: list = field(init=False, default_factory=list) 
    cached_subdomains: list = field(init=False, default_factory=list)
    cached_enumeration_result_count: int = field(init=False, default=0)
    
    def add(self, subdomain: str) -> None:
        """Add a subdomain to the cache"""
        if subdomain not in self.cached_subdomains:
            self.cached_subdomains.append(subdomain)
    
    def add_subdomain_uri(self, subdomain: str) -> None:
        if subdomain not in self.tmp_subdomains:
            self.tmp_subdomains.append(subdomain)
    
    def check_if_ip_already_found_and_return_result(self, ip) -> dict | None:
        """Check if the given ip is already in the cache"""
        if self.cached_subdomains:
            result = list(filter(lambda s: s.get('ip') == ip, self.cached_subdomains))
            if len(result) > 0:
                return result[0]
        return []
    
    def check_if_uri_already_found_and_return_result(self, uri) -> dict | None:
        """Check if the given ip is already in the cache"""
        if self.tmp_subdomains:
            result = list(filter(lambda s: s == uri, self.tmp_subdomains))
            if len(result) > 0:
                return result[0]
        return []
    
    