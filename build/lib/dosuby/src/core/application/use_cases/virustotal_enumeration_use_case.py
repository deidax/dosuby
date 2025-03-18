from dosuby.src.core.domain.target import Target
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator

class VirustotalEnumerationUseCase:
    """This is the Virustotal Enumeration Use Case.\n
    it will be used to enumerate subdomains using virustotal
    """
    
    def __init__(self, virustotal: SubdomainEnumerator) -> None:
        """Inject an enumerator module

        Args:
            virustotal (SubdomainEnumerator): subdomain enumerator
        """
        
        if not isinstance(virustotal, SubdomainEnumerator):
            raise ValueError(f'virustotal param should be a SubdomainEnumerator instance, not a {type(virustotal)}')
        
        self._virustotal = virustotal
    
    def execute(self, target: Target):
        """Execute method will run the enumeration process

        Args:
            target (Target): url or domain to enumerate
        """
        
        if not isinstance(target, Target):
            raise ValueError(f'target param should be a Target instance, not a {type(target)}.')
        
        self._virustotal.target_uri = target.target_uri.uri
        
        return self._virustotal.run()
    