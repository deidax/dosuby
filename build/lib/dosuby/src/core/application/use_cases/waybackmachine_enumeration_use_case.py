from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class WaybackmachineEnumerationUseCase:
    """This is the Waybackmachine Enumeration Use Case.\n
    it will be used to enumerate subdomains using waybackmachine
    """
    
    def __init__(self, waybackmachine: SubdomainEnumerator) -> None:
        """Inject an enumerator module

        Args:
            waybackmachine (SubdomainEnumerator): subdomain enumerator
        """
        
        if not isinstance(waybackmachine, SubdomainEnumerator):
            raise ValueError(f'waybackmachine param should be a SubdomainEnumerator instance, not a {type(waybackmachine)}')
        
        self._waybackmachine = waybackmachine
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._waybackmachine.target_uri = target.target_uri.uri
        
        return self._waybackmachine.run()
    