from abc import ABC, abstractmethod


class ReportRepo(ABC):
    
    @abstractmethod
    def read_report(self):
        NotImplementedError("read_report is not implemented")