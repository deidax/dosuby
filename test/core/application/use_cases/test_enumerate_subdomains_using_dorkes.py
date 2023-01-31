import pytest
from src.core.application.input_dtos.target_input_dto import TargetInputDTO
from src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from src.interfaces.dork import Dork

fake_uri = 'sometext.test'


fake_subdomains = ['fake.sometext.test', 'dork.sometext.test']

def test_enumerate_using_invalid_dork_use_case():
    
    
    fake_dork = 'fake dork'
    
    with pytest.raises(ValueError):
        DorksEnumerationUseCase(dork=fake_dork)


def test_enumerate_using_dorks_use_case():
    
    target_input = TargetInputDTO(uri=fake_uri)
    
    fake_dork = Dork()
    
    target_subdomains_use_case = DorksEnumerationUseCase(dork=fake_dork)
    
    target_subdomains_result = target_subdomains_use_case.execute(target=target_input)
    
    assert target_subdomains_result == fake_subdomains

def test_invalid_target_dto_input_in_dorks_use_case_execute():
    
    invalid_target_input = 'Invalid target DTO'
    
    fake_dork = Dork()
    
    target_subdomains_use_case = DorksEnumerationUseCase(dork=fake_dork)
    
    with pytest.raises(ValueError):
        target_subdomains_use_case.execute(target=invalid_target_input)