from dataclasses import dataclass, field
from src.interfaces.domain_serializer import DomainSerializer


@dataclass
class Subdomain:
    
    subdomain_serializer: DomainSerializer
    subdomain_uri: str = field(init=True)
    
    @property
    def subdomain_uri(self) -> list:
        return self._subdomain_uri
    
    @subdomain_uri.setter
    def subdomain_uri(self, value: str) -> None:
        if self.subdomain_serializer:
            self._subdomain_uri = self.subdomain_serializer.serialize(value)
        else:
            self._subdomain_uri = value
    
    
    def __eq__(self, __o: object) -> bool:
        return self.subdomain_uri == __o.subdomain_uri
    
    def __iter__(self):
        yield {
            'subdomain_uri': self.subdomain_uri,
        }
    
    # def __iter__(self):
    #     yield self.get_subdomain_as_dict()
    
  
    