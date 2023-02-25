from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton

@dataclass
class Cache(metaclass=Singleton):
    """Cache ips to use in real time execution
    """
    
    cached_subdomains: list = field(init=False, default_factory=list)
    
    def add(self, subdomain: str) -> None:
        """Add a subdomain to the cache"""
        if subdomain not in self.cached_subdomains:
            self.cached_subdomains.append(subdomain)
    
    def check_if_ip_already_found_and_return_result(self, ip) -> dict | None:
        """Check if the given ip is already in the cache"""
        if self.cached_subdomains:
            result = list(filter(lambda s: s.get('ip') == ip, self.cached_subdomains))
            if len(result) > 0:
                return result[0]
        return []
    
    