from dataclasses import dataclass, field
from src.interfaces.domain_serializer import DomainSerializer
from src.core.application.decorators.decorators import *

@dataclass
class Subdomain:
    
    subdomain_serializer: DomainSerializer
    subdomain_uri: str = field(init=True)
    _subdomain_ip: str = field(init=False, default='')
    _subdomain_hostname: str = field(init=False, default='')
    
    @property
    def subdomain_uri(self) -> str:
        return self._subdomain_uri
    
    @subdomain_uri.setter
    def subdomain_uri(self, value: str) -> None:
        if self.subdomain_serializer:
            self._subdomain_uri = self.subdomain_serializer.serialize(value)
            self._subdomain_ip = self.subdomain_uri
        else:
            self._subdomain_uri = value
    
    
    @property
    @get_ip
    def subdomain_ip(self) -> str:
        return self._subdomain_ip
    
    
    @property
    @get_hostname
    @get_ip
    def subdomain_hostname(self) -> str:
        return self._subdomain_hostname
    
    
    
    
    def __eq__(self, __o: object) -> bool:
        return self.subdomain_uri == __o.subdomain_uri
    
    
    
  
    