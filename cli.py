from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler


def main():
    
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    
    print('dosuby version:', version)
    print('\n')
    uri = 'uca.ma'
    
    try:
        
        yahoo = YahooDorkHandler()
        google = GoogleDorkHandler(next_handler=yahoo)
    
        google.handle(uri=uri)
        
    
    except Exception as ex:
        print(ex)
    


if __name__ == "__main__":
    main()
