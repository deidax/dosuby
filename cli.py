from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler
from src.handlers.cli.duckduckgo_dork_handler import DuckduckgoDorkHandler
from src.handlers.cli.brave_dork_handler import BraveDorkHandler
from src.handlers.cli.aol_dork_handler import AolDorkHandler
from src.handlers.cli.crt_search_handler import CrtSearchHandler
from src.core.domain.enumeration_reporte import EnumerationReporte

def main():
    
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    
    print('dosuby version:', version)
    print('\n')
    # uri = 'algerac.dz'
    # uri = 'uca.ma'
    uri = 'univ-alger.dz'
    
    try:
        
        yahoo = YahooDorkHandler()
        duckduckgo = DuckduckgoDorkHandler(next_handler=yahoo)
        google = GoogleDorkHandler(next_handler=duckduckgo)
        brave = BraveDorkHandler(next_handler=google)
        aol = AolDorkHandler(next_handler=brave)
        crt = CrtSearchHandler(next_handler=aol)
        
    # yahoo = YahooDorkHandler()
    # google = GoogleDorkHandler(next_handler=yahoo)
    # crt = CrtSearchHandler(next_handler=google)
    
        crt.handle(uri=uri)
        
        print('report--->')
        report = EnumerationReporte()
        print(report.report_subdomains)

    except Exception as ex:
        print(ex)
    


if __name__ == "__main__":
    main()
