from abc import ABC, abstractmethod

class EnumerationStrategy(ABC):
    
    @abstractmethod
    def enumeration_process(self, subdomains_links) -> list:
        """This class manage the logic for enumeration

        Args:
            subdomains_links (Generator): link generator

        Returns:
            list: list of enumeration result
        """
        pass