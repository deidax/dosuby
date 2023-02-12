from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler
from src.handlers.cli.duckduckgo_dork_handler import DuckduckgoDorkHandler
from src.handlers.cli.brave_dork_handler import BraveDorkHandler
from src.handlers.cli.aol_dork_handler import AolDorkHandler

def main():
    
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    
    print('dosuby version:', version)
    print('\n')
    uri = 'uca.ma'
    
    try:
        
        yahoo = YahooDorkHandler()
        google = GoogleDorkHandler(next_handler=yahoo)
        # duckduckgo = DuckduckgoDorkHandler(next_handler=google)
        # brave = BraveDorkHandler(next_handler=duckduckgo)
        # aol = AolDorkHandler(next_handler=brave)
        
        google.handle(uri=uri)
        
    
    except Exception as ex:
        print(ex)
    


if __name__ == "__main__":
    main()
