from abc import ABC,abstractmethod

class DomainSerializer(ABC):
    
    @abstractmethod
    def serialize(self, uri: str):
        pass