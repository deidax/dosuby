from dataclasses import dataclass, field


@dataclass
class Temp:
    """This is a class that holds temp variables
    """

    enumeration_module_result_count: int = field(init=False, default=0)