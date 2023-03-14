from abc import ABC, abstractmethod
from src.core.domain.config import Config
from src.core.domain.cache import Cache
import logging

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
    
    def display_result_count(self):
        cache = Cache()
        r_c = cache.cached_enumeration_result_count
        logging.info(f"{'-'*6}[SUBDOMAINS FOUND:    {r_c}]{'-'*6}")