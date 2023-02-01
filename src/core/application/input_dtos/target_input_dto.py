from dataclasses import dataclass
from src.core.application.validators.validate_target_input import ValidateTargetInput
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

@dataclass
class TargetInputDTO:
    """This dataclass with manage the target inputs and parameters\n
        like the uri we would like to enumerat, what search engine dork we like to use...
    """
    uri: str

    def __post_init__(self):
        self.uri = ValidateTargetInput.extract_domain(target_uri=self.uri)
        if self.uri is False:
            raise InvalidTargetException(error={'parameter': 'uri', 'message': 'Invalid target uri'})