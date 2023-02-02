from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
from src.adapter.dorks.yahoo_dorks_adapter import YahooDorksAdapter
from src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException


def main():
    
    try:
        target_input_dto = TargetInputDTO(uri='uca.ma')
    except InvalidTargetException as ex:
        print(ex)
        return
    
    try:
        """
        google_dork = GoogleDorksAdapter()
        target_google_dork_usecase = DorksEnumerationUseCase(dork=google_dork)
        result = target_google_dork_usecase.execute(target=target_input_dto)
        """
        yahoo_dork = YahooDorksAdapter()
        target_yahoo_dork_usecase = DorksEnumerationUseCase(dork=yahoo_dork)
        result = target_yahoo_dork_usecase.execute(target=target_input_dto)
        
        print(result)
    except Exception as ex:
        print(ex)
        return


if __name__ == "__main__":
    main()
