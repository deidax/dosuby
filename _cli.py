from rich.console import Console
import inquirer
import re
from src.core.domain.config import Config
from src.handlers.cli.google_dork_handler import GoogleDorkHandler
from src.handlers.cli.yahoo_dork_handler import YahooDorkHandler
from src.handlers.cli.duckduckgo_dork_handler import DuckduckgoDorkHandler
from src.handlers.cli.brave_dork_handler import BraveDorkHandler
from src.handlers.cli.aol_dork_handler import AolDorkHandler
from src.handlers.cli.crt_search_handler import CrtSearchHandler
from src.handlers.cli.bing_dork_handler import BingDorkHandler
from src.handlers.cli.anubis_dork_handler import AnubisHandler
from src.handlers.cli.ask_dork_handler import AskDorkHandler
from src.handlers.cli.alientvault_handler import AlientvaultHandler
from src.handlers.cli.hackertarget_handler import HackertargetHandler
from src.handlers.cli.waybackmachine_handler import WaybackmachineHandler
from src.handlers.cli.virustotal_handler import VirustotalHandler
from src.interfaces.handler import Handler
from src.repositories.cli_report_repo import CliReportRepo
from typing import List
import logging

def main():
    """Main function for the interactive CLI."""
    
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
    
    regex = r"^[a-z]{2,}\.[a-z]{2,}$"
    handlers = [
        {'name':'Google', 'value': GoogleDorkHandler},
        {'name':'Yahoo', 'value': YahooDorkHandler},
        {'name':'Duckduckgo', 'value': DuckduckgoDorkHandler},
        {'name':'Brave', 'value': BraveDorkHandler},
        {'name':'Aol', 'value': AolDorkHandler},
        {'name':'Bing', 'value': BingDorkHandler},
        {'name':'Ask', 'value': AskDorkHandler},
        {'name':'Crt Search', 'value': CrtSearchHandler},
        {'name':'Anubis', 'value': AnubisHandler},
        {'name':'AlientVault', 'value': AlientvaultHandler},
        {'name':'HackerTarget', 'value': HackertargetHandler},
        {'name':'WaybackMachine', 'value': WaybackmachineHandler},
        {'name':'VirusTotal', 'value': VirustotalHandler}
    ]
    
    # Extract the 'name' keys from the list of dictionaries
    handlers_choices = [handler['name'] for handler in handlers]
    
    questions = [
    inquirer.Text('TLD', message="What's the domain to enumerate",
                        validate=lambda _, x: re.match(regex, x)
                ),
    inquirer.Checkbox('handlers',
                        message="Choose methods to use for the enumeration",
                        choices=handlers_choices,
                        ),
    inquirer.Confirm("scanning_modules", message="Do you want to scan subdomains?",)
    ]
    
    answers = inquirer.prompt(questions)
    
    target_uri = answers.get('TLD')
    selected_handlers = answers.get('handlers')
    config.scanning_modules = answers.get('scanning_modules')
    
    found_handlers: List[dict] = []

    for handler in handlers:
        if handler['name'] in selected_handlers:
            found_handlers.append(handler)

    if found_handlers:
        try:
            
            handlers_selected: List[Handler] = []
            handlers_selected_objects: List[Handler] = []
            
            for handler in found_handlers:
                handler_class_name = handler.get('value')
                handlers_selected.append(handler_class_name)
                
            for handler_selected_class_name in reversed(handlers_selected):
                handler_object: Handler = None
                next_handler = None
                if handlers_selected_objects:
                    next_selected_handler = handlers_selected_objects[-1]
                    next_handler = next_selected_handler
                    
                handler_object = handler_selected_class_name(next_handler=next_handler)
                handlers_selected_objects.append(handler_object)
            
            handlers_to_use = handlers_selected_objects[::-1]
            handler_starter = handlers_to_use[0]
            
            s = f"\n{'-'*10}[Starting...]{'-'*10}"
            print(s)
            handler_starter.handle(uri=target_uri)
            report = CliReportRepo()
            report.read_report()
            
        except Exception as ex:
            print(ex)
            
            
    else:
        print("Handlers not found.")


if __name__ == "__main__":
    main()
