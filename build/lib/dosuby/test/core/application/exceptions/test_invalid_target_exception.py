import pytest
from unittest import mock
from dosuby.src.core.application.exceptions.invalid_target_input_exception import InvalidTargetException


def test_invalid_target_input_error():
    
    req = mock.Mock()
    
    req.errors = [{'parameter': 'target', 'message': 'Invalid'}]
    
    ex = InvalidTargetException()
    
    ex.add_error('target', 'Invalid')
    
    assert req.errors == ex.errors
    
    assert bool(ex) is True
    
    with pytest.raises(Exception):
        ex.errors = [{'parameter': 'target', 'message': 'Invalid'}]

def test_invalid_target_input_error_string():
    
    req = mock.Mock()
    
    def mock_load_invalid_target():
        req.target = None
        if req.target is None:
            raise InvalidTargetException(error={'parameter': 'target', 'message': 'Invalid'})
        return 
        
    req.load_target.side_effect = mock_load_invalid_target
    
    with pytest.raises(InvalidTargetException, match="target: Invalid"):
        req.load_target()
