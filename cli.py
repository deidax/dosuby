from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler


def main():
    
    
    yahoo = YahooDorkHandler()
    google = GoogleDorkHandler(next_handler=yahoo)
    
    uri = 'uca.ma'
    
    google.handle(uri=uri)


if __name__ == "__main__":
    main()
