from dataclasses import dataclass, field
from typing import List

@dataclass
class Target:
    
    subdomains: List[str] = field(default_factory=lambda: [])
    
    def add_subdomain(self, subdomain: str):
        if subdomain not in self.subdomains:
            self.subdomains.append(subdomain)
    