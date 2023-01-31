import pytest
from src.core.application.input_dtos.target_input_dto import TargetInputDTO

fake_uri = 'sometext.test'

def test_target_uri_existes():
    fake_target = TargetInputDTO(uri=fake_uri)
    
    assert fake_target.uri == fake_uri