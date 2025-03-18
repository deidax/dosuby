from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class AlientvaultEnumerationUseCase:
    """This is the Alientvault Enumeration Use Case.\n
    it will be used to enumerate subdomains using alientvault
    """
    
    def __init__(self, alientvault: SubdomainEnumerator) -> None:
        """Inject an enumerator module

        Args:
            alientvault (SubdomainEnumerator): subdomain enumerator
        """
        
        if not isinstance(alientvault, SubdomainEnumerator):
            raise ValueError(f'alientvault param should be a SubdomainEnumerator instance, not a {type(alientvault)}')
        
        self._alientvault = alientvault
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._alientvault.target_uri = target.target_uri.uri
        
        return self._alientvault.run()
    