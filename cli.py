from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler


def main():
    
    with open('version.txt', 'r') as f:
        version = f.read().strip()
    
    print('version:', version)
    
    yahoo = YahooDorkHandler()
    google = GoogleDorkHandler(next_handler=yahoo)
    
    uri = 'uca.ma'
    
    google.handle(uri=uri)


if __name__ == "__main__":
    main()
