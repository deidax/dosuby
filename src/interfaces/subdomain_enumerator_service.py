from abc import ABC, abstractmethod

class SubdomainEnumeratorService(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @staticmethod
    @abstractmethod
    def read(cls, uri: str):
        """Read the dorks data to get the domain subdomains using dorks

        Args:
            uri (str): uri target
        """
        pass