from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class CrtEnumerationUseCase:
    """This is the SubdomainEnumerator Enumeration Use Case.\n
    it will be used to enumerate subdomains using search engine dorks
    """
    
    def __init__(self, crt: SubdomainEnumerator) -> None:
        """Inject a search engine dork to be used

        Args:
            crt (SubdomainEnumerator): crt search.Must implement SubdomainEnumerator interface
        """
        
        if not isinstance(crt, SubdomainEnumerator):
            raise ValueError(f'crt param should be a SubdomainEnumerator instance, not a {type(crt)}')
        
        self._crt = crt
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._crt.target_uri = target.target_uri.uri
        
        return self._crt.run()
    