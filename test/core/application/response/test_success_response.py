import pytest
from src.core.application.response.cli.success_response_builder import SuccessResponseBuilder

# def test_cli_success_response_builder():
    
#     cli_success_response = SuccessResponseBuilder().set_value('sub.domain.test')\
#                                                    .set_response_message('Subdomain Found!')\
#                                                    .build_response()
    
    
#     assert cli_success_response.get_response() == f"Status:    OK\n"\
#                                                   f"Message:   Subdomain Found!\n"\
#                                                   f"Subdomain: sub.domain.test\n"\
#                                                   f"{'-'*10}\n"