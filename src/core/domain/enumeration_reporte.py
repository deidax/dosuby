from dataclasses import dataclass, field
from src.interfaces.singleton import Singleton

@dataclass
class EnumerationReporte(metaclass=Singleton):
    """Cache results to use in real time execution
    """
    
    report_subdomains: list = field(init=False, default_factory=list)
    
    def add(self, subdomain) -> None:
        self.report_subdomains.append(subdomain)