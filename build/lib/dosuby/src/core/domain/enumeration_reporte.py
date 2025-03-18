from dataclasses import dataclass, field
from dosuby.src.interfaces.singleton import Singleton


@dataclass
class EnumerationReporte(metaclass=Singleton):
    """Cache results to use in real time execution
    """

    report_subdomains: list = field(init=False, default_factory=list)

    def add(self, subdomain: list) -> None:
        self.report_subdomains.extend(subdomain)
