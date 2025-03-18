from dosuby.src.services.dorks.cli.google_dork_cli_service import GoogleDorkCliService
from dosuby.src.interfaces.success_response import SuccessResponse


def test_google_service_creation():
    
    google_service = GoogleDorkCliService()
    
    assert type(google_service.success_response) is SuccessResponse



def test_google_process_enumeration_dork(monkeypatch):
    
    moke_build_enumerator_result = ['domain1', 'domain2']
    
    monkeypatch.setattr(GoogleDorkCliService, 'build_enumerator', moke_build_enumerator_result)
    
    google_service = GoogleDorkCliService()
    
    process_result = google_service.process_enumerator(result=[])
    
    assert type(process_result) is SuccessResponse