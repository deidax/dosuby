from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class HackertargetEnumerationUseCase:
    """This is the Hackertarget Enumeration Use Case.\n
    it will be used to enumerate subdomains using hackertarget
    """
    
    def __init__(self, hackertarget: SubdomainEnumerator) -> None:
        """Inject an enumerator module

        Args:
            hackertarget (SubdomainEnumerator): subdomain enumerator
        """
        
        if not isinstance(hackertarget, SubdomainEnumerator):
            raise ValueError(f'hackertarget param should be a SubdomainEnumerator instance, not a {type(hackertarget)}')
        
        self._hackertarget = hackertarget
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._hackertarget.target_uri = target.target_uri.uri
        
        return self._hackertarget.run()
    