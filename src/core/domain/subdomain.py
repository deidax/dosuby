from dataclasses import dataclass, field
from src.interfaces.domain_serializer import DomainSerializer
from src.core.application.decorators.decorators import *

@dataclass
class Subdomain:
    
    subdomain_serializer: DomainSerializer
    subdomain_uri: str = field(init=True)
    subdomain_link: str = field(init=False, default='')
    open_ports: list = field(init=False, default_factory=list)
    _subdomain_uri: str = field(init=False, default='')
    _subdomain_ip: str = field(init=False, default='')
    _subdomain_hostname: str = field(init=False, default='')
    _subdomain_open_ports_from_uri: str = field(init=False, default='')
    
    
    
    @property
    def subdomain_uri(self) -> str:
        return self._subdomain_uri
    
    @subdomain_uri.setter
    def subdomain_uri(self, value: str) -> None:
        
        if self.subdomain_serializer:
            
            self._subdomain_uri = self.subdomain_serializer.serialize(value)
            
            # assign subdomain_uri to get ip and open ports for the asseigned subdomain uri
            self._subdomain_ip = self.subdomain_uri
            self._subdomain_open_ports_from_uri = {'ip':self.subdomain_ip,'uri': self.subdomain_uri}
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
    
    
    @property
    @add_to_list('open_ports')
    @get_open_ports
    def subdomain_open_ports_from_uri(self) -> list:
        """Scan for open ports

        Returns:
            list: open ports list
        """
        return self._subdomain_open_ports_from_uri
    
    
    # @property
    # def subdomain_link_from_uri(self) -> str:
    #     return self._subdomain_link_from_uri

    
    
    
    def __eq__(self, __o: object) -> bool:
        return self.subdomain_uri == __o.subdomain_uri
    
    
    def get_cached_data(self) -> dict:
        """Get the subdomain cached data

        Returns:
            dict: cached subdomain data
        """
        return {
            'ip': self.subdomain_ip,
            'link': self.subdomain_link,
            'open_ports': self.subdomain_open_ports_from_uri
        }
    
    