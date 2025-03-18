from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class DorksEnumerationUseCase:
    """This is the SubdomainEnumerator Enumeration Use Case.\n
    it will be used to enumerate subdomains using search engine dorks
    """
    
    def __init__(self, dork: SubdomainEnumerator) -> None:
        """Inject a search engine dork to be used

        Args:
            dork (SubdomainEnumerator): search engine dork (GoogleDork, BingDork...).Must implement SubdomainEnumerator interface
        """
        
        if not isinstance(dork, SubdomainEnumerator):
            raise ValueError(f'dork param should be a SubdomainEnumerator instance, not a {type(dork)}')
        
        self._dork = dork
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._dork.target_uri = target.target_uri.uri
        
        return self._dork.run()
    