from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton
from src.interfaces.domain_serializer import DomainSerializer
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from typing import List

@dataclass
class Target(metaclass=Singleton):
    """Target Singleton

    Args:
        metaclass (Singleton): Defaults to Singleton.

    """
    
    target_uri: str
    _subdomain: str = field(init=False)
    _subdomains: List[str] = field(default_factory=list, init=False)
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
    
    @property
    def subdomains(self) -> list:
        return self._subdomains
    
    @subdomains.setter
    def subdomains(self, value):
        self._subdomains.append(value)
    
    
    def __post_init__(self):
         self.target_uri = TargetInputDTO(uri=self.target_uri)
    
    def add_subdomain(self, subdomain: str) -> bool:
        self.subdomain = subdomain
        if self.subdomain not in self.subdomains and self.target_uri.check_if_result_is_accurate(self.subdomain):
            self.subdomains = self._subdomain
            return True
        
        return False
    