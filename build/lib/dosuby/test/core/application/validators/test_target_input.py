import pytest
from dosuby.src.core.application.validators.validate_target_input import ValidateTargetInput


def test_if_target_is_a_domain():
    
    fake_target_url = 'https://www.example.com'
    
    target_extracted_domain = ValidateTargetInput.extract_domain(target_uri=fake_target_url)
    
    assert target_extracted_domain == 'example.com'

def test_if_target_is_invalid():
    
    fake_target_url = "not-a-domain"
    
    target_extracted_domain = ValidateTargetInput.extract_domain(target_uri=fake_target_url)
    
    assert target_extracted_domain is False