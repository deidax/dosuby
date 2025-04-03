from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton
from dosuby.src.interfaces.domain_serializer import DomainSerializer
from dosuby.src.core.application.input_dtos.target_input_dto import TargetInputDTO
from .subdomain import Subdomain
from typing import List
from dosuby.src.core.application.decorators.enumeration_decorators import *
from dosuby.src.core.application.decorators.loggers_decorators import *
from .config import Config

@dataclass
class Target(metaclass=Singleton):
    """Target Singleton

    Args:
        metaclass (Singleton): Defaults to Singleton.

    """
    
    target_uri: str
    _subdomain: Subdomain = field(init=False)
    _subdomains: List[Subdomain] = field(init=False,default_factory=list)
    config: Config = field(init=False)
    subdomain_serializer: DomainSerializer = None
    skip_logging: bool = field(init=False, default=False)
    _subdomain_count: int = field(init=False, default=0)
    
    
    def __post_init__(self):
        self.target_uri = TargetInputDTO(uri=self.target_uri)
        self.config = Config()
    
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
    
    
   
    
    
    @info_subdomain_found('skip_logging')
    def add_subdomain(self, subdomain: str) -> bool:
        self.subdomain = subdomain
        
        if (
            not any(sub == self.subdomain for sub in self.subdomains) 
            and self.target_uri.check_if_result_is_accurate(self.subdomain.subdomain_uri)
        ):
            self.subdomains = self._subdomain
            self._subdomain_count = self._subdomain_count + 1
            return True
        
        return False
    
    @property
    def subdomains_count(self):
        return self._subdomain_count
    
    def subdomain_count_init(self):
        self._subdomain_count = 0
        
    
    
    @save_enumeration_report
    def get_target_intel(self):
       if self.config.scanning_modules:
           sub_dict = lambda s: {
                                    'subdomain_uri': s.subdomain_uri,
                                    'subdomain_ip': s.subdomain_ip,
                                    'subdomain_hostname': s.subdomain_hostname,
                                    'subdomain_open_ports': s.open_ports,
                                    'subdomian_cms': s.cms,
                                    'subdomain_webserver': s.webserver,
                                    'subdomain_vulnerabilities': s.cve_codes
                                }
       else:
           sub_dict = lambda s: {
                                    'subdomain_uri': s.subdomain_uri,
                                    'subdomain_ip': s.subdomain_ip,
                                }
           
       
       return [(sub_dict)(sub) for sub in self.subdomains]
    
    