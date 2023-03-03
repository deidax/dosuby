from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton
from src.interfaces.domain_serializer import DomainSerializer
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from .subdomain import Subdomain
from typing import List
from src.core.application.decorators.enumeration_decorators import *
from src.core.application.decorators.loggers_decorators import *

@dataclass
class Target(metaclass=Singleton):
    """Target Singleton

    Args:
        metaclass (Singleton): Defaults to Singleton.

    """
    
    target_uri: str
    _subdomain: Subdomain = field(init=False)
    _subdomains: List[Subdomain] = field(init=False,default_factory=list)
    subdomain_serializer: DomainSerializer = None
    skip_logging: bool = field(init=False, default=False)
    
    @property
    def subdomain(self) -> Subdomain:
        return self._subdomain
    
    @subdomain.setter
    def subdomain(self, value: str) -> None:
        self._subdomain = Subdomain(
                                subdomain_uri=value, 
                                subdomain_serializer=self.subdomain_serializer
                            )
    
    @property
    def subdomains(self) -> list:
        return self._subdomains
    
    @subdomains.setter
    @cache_subdomain
    def subdomains(self, value):
        self._subdomains.append(value)
    
    
    def __post_init__(self):
         self.target_uri = TargetInputDTO(uri=self.target_uri)
    
    
    @info_subdomain_found('skip_logging')
    def add_subdomain(self, subdomain: str) -> bool:
        self.subdomain = subdomain
        if not any(sub == self.subdomain for sub in self.subdomains) and self.target_uri.check_if_result_is_accurate(self.subdomain.subdomain_uri):
            self.subdomains = self._subdomain
            return True
        
        return False
    
    @save_enumeration_report
    def get_target_intel(self):
       
       sub_dict = lambda s: {
                            'subdomain_uri': s.subdomain_uri,
                            'subdomain_ip': s.subdomain_ip,
                            'subdomain_hostname': s.subdomain_hostname,
                            'subdomain_open_ports': s.open_ports,
<<<<<<< HEAD
                            'subdomian_cms': s.cms,
=======
                            'subdomain_webserver': s.subdomain_webserver
>>>>>>> ff1ae39 (setting up webserver scanning)
                        }
       
       return [(sub_dict)(sub) for sub in self.subdomains]
    