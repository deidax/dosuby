import pytest
from dosuby.src.core.application.input_dtos.target_input_dto import TargetInputDTO
from dosuby.src.core.application.use_cases.dorks_enumeration_use_case import DorksEnumerationUseCase
from dosuby.src.interfaces.subdomain_enumerator import SubdomainEnumerator
from dosuby.src.adapter.dorks.google_dorks_adapter import GoogleDorksAdapter
from unittest import mock

fake_uri = 'sometext.test'


fake_subdomains = ['fake.sometext.test', 'dork.sometext.test']

def test_enumerate_using_invalid_dork_use_case():
    
    
    fake_dork = 'fake dork'
    
    with pytest.raises(ValueError):
        DorksEnumerationUseCase(dork=fake_dork)


# def test_enumerate_using_google_dorks_use_case(monkeypatch):
    
#     # Create a fake google dorks enumeration result
#     def mock_google_dork_get_results(self):
#         return fake_subdomains
    
#     monkeypatch.setattr(GoogleDorksAdapter, 'get_results', mock_google_dork_get_results)
    
#     fake_google_dork = GoogleDorksAdapter()
    
#     # Inject the fake GoogleDorksAdapter
#     target_subdomains_use_case = DorksEnumerationUseCase(dork=fake_google_dork)
#     # Set a target uri
#     target_input = TargetInputDTO(uri=fake_uri)
#     # Inject the target DTO input
#     target_subdomains_result = target_subdomains_use_case.execute(target=target_input)
    
#     assert target_subdomains_result == fake_subdomains

def test_invalid_target_dto_input_in_dorks_use_case_execute():
    
    invalid_target_input = 'Invalid target DTO'
    
    fake_dork = GoogleDorksAdapter()
    
    target_subdomains_use_case = DorksEnumerationUseCase(dork=fake_dork)
    
    with pytest.raises(ValueError):
        target_subdomains_use_case.execute(target=invalid_target_input)