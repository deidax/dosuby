from dataclasses import dataclass, field
from src.interfaces.domain_serializer import DomainSerializer
from src.core.application.decorators.enumeration_decorators import *
from src.core.application.decorators.loggers_decorators import *
from typing import Any

@dataclass
class Subdomain:
    
    subdomain_serializer: DomainSerializer
    subdomain_uri: str = field(init=True)
    open_ports: list = field(init=False, default_factory=list)
    cms: Any = field(init=False)
    skip_logging: bool = field(init=False)
    _subdomain_cms: str = field(init=False, default='')
    _subdomain_uri: str = field(init=False, default='')
    _subdomain_ip: str = field(init=False, default='')
    _subdomain_hostname: str = field(init=False, default='')
    _subdomain_open_ports_from_uri: str = field(init=False, default='')
    _subdomain_webserver_from_ip: str = field(init=False, default='')
    
    
    
    @property
    def subdomain_uri(self) -> str:
        return self._subdomain_uri
    
    @subdomain_uri.setter
    def subdomain_uri(self, value: str) -> None:
        
        self.skip_logging = True
        
        if self.subdomain_serializer:
            
            
            self._subdomain_uri = self.subdomain_serializer.serialize(value)
            
            # assign subdomain_uri to get ip and open ports for the asseigned subdomain uri
            self._subdomain_ip = self.subdomain_uri
            self._subdomain_open_ports_from_uri = {'ip':self.subdomain_ip,'uri': self.subdomain_uri}
            self._subdomain_cms = {'ip':self.subdomain_ip,'uri': self.subdomain_uri}
            self._subdomain_webserver_from_ip = {'ip':self.subdomain_ip,'uri': self.subdomain_uri}
        else:
            self._subdomain_uri = value

        self.skip_logging = False
        
    
    @property
    @info_ip_found('skip_logging')
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
    @info_port_scanning('skip_logging')
    def subdomain_open_ports_from_uri(self) -> list:
        """Scan for open ports

        Returns:
            list: open ports list
        """
        return self._subdomain_open_ports_from_uri
    
    
    @property
<<<<<<< HEAD
    @save_cms('cms')
    @scan_for_cms
    @info_cms_scanning('skip_logging')
    def subdomain_cms(self):
        return self._subdomain_cms
=======
>>>>>>> origin/main
    @get_webserver
    def subdomain_webserver(self) -> str:
        """Scan for webserver

        Returns:
            list: webserver list
        """
        return self._subdomain_webserver_from_ip

    
    
    
    def __eq__(self, __o: object) -> bool:
        return self.subdomain_uri == __o.subdomain_uri
    
    
    def get_cached_data(self) -> dict:
        """Get the subdomain cached data

        Returns:
            dict: cached subdomain data
        """
        self.skip_logging = True
        
        cached_data = {
            'ip': self.subdomain_ip,
            'open_ports': self.subdomain_open_ports_from_uri,
        }
        
        self.skip_logging = False
        
        return cached_data
    
    