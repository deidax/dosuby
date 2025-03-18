import pytest
from dosuby.src.core.application.input_dtos.target_input_dto import TargetInputDTO
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException


def test_target_uri_existes():
    
    fake_uri = 'sometext.test'
    fake_target = TargetInputDTO(uri=fake_uri)
    
    assert fake_target.uri == fake_uri

def test_invalid_uri_input():
    
    invalid_fake_uri = 'invalid-uri-target'
    
    with pytest.raises(InvalidTargetException):
        fake_target = TargetInputDTO(uri=invalid_fake_uri)

def test_invalid_uri_with_correct_message():
    
    invalid_fake_uri = 'invalid-uri-target'
    
    with pytest.raises(InvalidTargetException, match="uri: Invalid target uri"):
        fake_target = TargetInputDTO(uri=invalid_fake_uri)
        