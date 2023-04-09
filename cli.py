from src.core.domain.config import Config
from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler
from src.handlers.cli.duckduckgo_dork_handler import DuckduckgoDorkHandler
from src.handlers.cli.brave_dork_handler import BraveDorkHandler
from src.handlers.cli.aol_dork_handler import AolDorkHandler
from src.handlers.cli.crt_search_handler import CrtSearchHandler
from src.handlers.cli.bing_dork_handler import BingDorkHandler
from src.core.domain.enumeration_reporte import EnumerationReporte
from src.handlers.cli.anubis_dork_handler import AnubisHandler
from src.handlers.cli.ask_dork_handler import AskDorkHandler
from src.handlers.cli.alientvault_handler import AlientvaultHandler
from src.handlers.cli.hackertarget_handler import HackertargetHandler
from src.handlers.cli.waybackmachine_handler import WaybackmachineHandler
from src.handlers.cli.virustotal_handler import VirustotalHandler
import logging

def main():
    
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    
    
    logging.basicConfig(
                level=logging.INFO, 
                format="%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
    
    
    config = Config()
    config.scanning_modules = False
    
    print('dosuby version:', version)
    print('\n')
    uri = 'californiacolleges.edu'
    uri = 'uca.ma'
    
    try:
        
        # virustotal = VirustotalHandler()
        waybackmachine = WaybackmachineHandler()
        # hacker_target = HackertargetHandler(next_handler=waybackmachine)
        # alient_vault = AlientvaultHandler(next_handler=hacker_target)
        # aol = AolDorkHandler(next_handler=alient_vault)
        # crt = CrtSearchHandler(next_handler=aol)
        # anubis = AnubisHandler(next_handler=crt)
        # bing = BingDorkHandler(next_handler=anubis)
        # yahoo = YahooDorkHandler(next_handler=bing)
        # duckduckgo = DuckduckgoDorkHandler(next_handler=yahoo)
        # google = GoogleDorkHandler(next_handler=duckduckgo)
        # brave = BraveDorkHandler(next_handler=google)
        ask = AskDorkHandler()

        
    # yahoo = YahooDorkHandler()
    # google = GoogleDorkHandler(next_handler=yahoo)
    # crt = CrtSearchHandler(next_handler=google)
    
        waybackmachine.handle(uri=uri)
        
        print('report--->')
        report = EnumerationReporte()
        print(report.report_subdomains)

    except Exception as ex:
        print(ex)
    


if __name__ == "__main__":
    main()
