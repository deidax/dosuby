from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton

@dataclass
class Cache(metaclass=Singleton):
    """Cache results to use in real time execution
    """
    
    cache_subdomais: list = field(init=False, default_factory=list)
    
    
    def check_if_ip_already_found(self, ip):
        """Check if the given ip is already in the cache"""
        if self.cache_subdomais:
            result = list(filter(lambda s: s.get('subdomain_ip') == ip, self.cache_subdomais))
            return result
        return False
    
    def search_for_ip_port(self, ip):
        """Returns ports from cache for a given IP"""
        result = list(filter(lambda s: s.get('subdomain_ip') == ip, self.cache_subdomais))
        if len(result) > 0:
            return result[0].get('subdomain_open_ports')
        else:
            return None
        