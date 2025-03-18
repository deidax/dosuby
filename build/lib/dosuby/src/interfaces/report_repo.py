from abc import ABC, abstractmethod
from dosuby.src.core.domain.config import Config

class ReportRepo(ABC):
    
    def __init__(self) -> None:
        super().__init__()
        self.config = Config()
    
    @abstractmethod
    def read_report(self):
        NotImplementedError("read_report is not implemented")