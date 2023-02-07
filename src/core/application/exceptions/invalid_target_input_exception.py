

class InvalidTargetException(Exception):
    
    def __init__(self,error={}, *args: object) -> None:
        """This class with customize the input params exceptions

        Args:
            error (dict, optional): error value {'parameter': 'param_example', 'message': 'exception message example'}. Defaults to {}.
        """
        
        super().__init__(*args)
        self._errors = []
        if bool(error): self._errors.append(error)
    
    
    def add_error(self, parameter: str, message: str):
        """Append new errors

        Args:
            parameter (str): parameter name subject of the error
            message (str): exception error message
        """
        self._errors.append({'parameter': parameter, 'message': message})
    
    @property
    def errors(self):
        return self._errors
    
    
    def __bool__(self):
        return len(self.errors) > 0

    def __str__(self) -> str:
        # building a custom error message
        if len(self.errors) < 1: return self
        err_m = ''
        for err in self.errors:
            err_m = err_m+"{0}: {1}\n".format(err['parameter'], err['message'])
        
        return err_m[:-1]
    