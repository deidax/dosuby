from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler


def main():
    
    uri = 'uca-ma'
    
    google = GoogleDorkHandler()
    yahoo = YahooDorkHandler()
    
    google.set_next(handler=yahoo)
    
    google.handle(uri=uri)
    yahoo.handle(uri=uri)
    


if __name__ == "__main__":
    main()
