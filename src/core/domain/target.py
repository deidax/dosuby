from dataclasses import dataclass, field
from src.interfaces.domain_serializer import DomainSerializer
from typing import List

@dataclass
class Target:
    
    _subdomain: str = field(init=False)
    subdomains: List[str] = field(default_factory=list)
    subdomain_serializer: DomainSerializer = None
    
    @property
    def subdomain(self) -> str:
        return self._subdomain
    
    @subdomain.setter
    def subdomain(self, value: str) -> None:
        if self.subdomain_serializer:
            self._subdomain = self.subdomain_serializer.serialize(value)
        else:
            self._subdomain = value
    
    
    def add_subdomain(self, subdomain: str) -> bool:
        print(subdomain)
        self.subdomain = subdomain
        if subdomain not in self.subdomains:
            self.subdomains.append(self._subdomain)
            return True
        
        return False
    