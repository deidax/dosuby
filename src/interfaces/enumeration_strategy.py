from abc import ABC, abstractmethod
from src.core.domain.config import Config

class EnumerationStrategy(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.config = Config()
    
    @abstractmethod
    def enumeration_process(self, subdomains_links) -> list:
        """This class manage the logic for enumeration

        Args:
            subdomains_links (Generator): link generator

        Returns:
            list: list of enumeration result
        """
        pass
    
    
    
    def display_result(self, result: str):
        if self.config.scanning_modules:
            print(result)