from dataclasses import dataclass
from dosuby.src.core.application.validators.validate_target_input import ValidateTargetInput
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException

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
    
    def check_if_result_is_accurate(self, subdomain: str):
        """This method will check if the subdomain found is really belongs to the target domain or not
        

        Args:
            subdomain (str): the enumerated subdomain
        """
        return (
            self.uri
            in subdomain
            and '*' not in subdomain
            and f"www.{self.uri}" != subdomain
            and self.uri != subdomain
            and subdomain.endswith(f".{self.uri}")
        )
        