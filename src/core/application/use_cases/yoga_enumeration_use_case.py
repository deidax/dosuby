from src.core.domain.target import Target
from src.interfaces.subdomain_enumerator import SubdomainEnumerator

class YogaEnumerationUseCase:
    """This is the Yoga Enumeration Use Case.\n
    it will be used to enumerate subdomains using yoga
    """
    
    def __init__(self, yoga: SubdomainEnumerator) -> None:
        """Inject an enumerator module

        Args:
            yoga (SubdomainEnumerator): subdomain enumerator
        """
        
        if not isinstance(yoga, SubdomainEnumerator):
            raise ValueError(f'yoga param should be a SubdomainEnumerator instance, not a {type(yoga)}')
        
        self._yoga = yoga
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._yoga.target_uri = target.target_uri.uri
        
        return self._yoga.run()
    