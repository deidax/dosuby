from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.interfaces.dork import Dork

class DorksEnumerationUseCase:
    """This is the Dork Enumeration Use Case.\n
    it will be used to enumerate subdomains using search engine dorks
    """
    
    def __init__(self, dork: Dork) -> None:
        """Inject a search engine dork to be used

        Args:
            dork (Dork): search engine dork (GoogleDork, BingDork...).Must implement Dork interface
        """
        
        if not isinstance(dork, Dork):
            raise ValueError(f'dork param should be a Dork instance, not a {type(dork)}')
        
        self._dork = dork
    
    def execute(self, target: TargetInputDTO):
        """Execute method will run the enumeration process

        Args:
            target (TargetInputDTO): url or domain to enumerate
        """
        
        if not isinstance(target, TargetInputDTO):
            raise ValueError(f'target param should be a TargetInputDTO instance, not a {type(target)}.')
        
        self._dork.target_uri = target.uri
        
        return self._dork.get_results()
    