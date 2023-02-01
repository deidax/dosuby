from src.interfaces.dork import Dork

class GoogleDorksAdapter(Dork):
    
    def __init__(self) -> None:
        """This class will manage the enumeration logic using the Google dorks

        """
        super().__init__()
    
    def _set_dork_queries(self, querys: list):
        """Set the Google query that will be used in the enumeration process

        Args:
            query (str): should be a google dork

        Returns:
            _type_: None
        """
        return super()._set_dork_queries(querys)
    
    def get_results(self) -> dict:
        return super().get_results()