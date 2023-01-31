import pytest
from src.core.application.input_dtos.target_input_dto import TargetInputDTO

fake_uri = 'sometext.test'

fake_subdomains = ['fake.sometext.test', 'dork.sometext.test']

def test_enumerate_using_dorks_use_case():
    
    target_input = TargetInputDTO(uri=fake_uri)
    
    target_subdomains_use_case = DorkEnumerationUseCase(dork=fake_dork)
    
    target_subdomains_result = target_subdomains_use_case.execute(target=target_input)
    
    assert target_subdomains_result == fake_subdomains