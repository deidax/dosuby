from dataclasses import dataclass

@dataclass
class Target:
    
    subdomains: list[str]
    
    def add_subdomain(self, subdomain: str):
        if subdomain not in self.subdomains:
            self.subdomains.append(subdomain)
    