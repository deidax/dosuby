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
        {'id': '1','name':'Google', 'value': GoogleDorkHandler},
        {'id': '2','name':'Yahoo', 'value': YahooDorkHandler},
        {'id': '3','name':'Duckduckgo', 'value': DuckduckgoDorkHandler},
        {'id': '4','name':'Brave', 'value': BraveDorkHandler},
        {'id': '5','name':'Aol', 'value': AolDorkHandler},
        {'id': '6','name':'Bing', 'value': BingDorkHandler},
        {'id': '7','name':'Ask', 'value': AskDorkHandler},
        {'id': '8','name':'Crt Search', 'value': CrtSearchHandler},
        {'id': '9','name':'Anubis', 'value': AnubisHandler},
        {'id': '10','name':'AlientVault', 'value': AlientvaultHandler},
        {'id': '11','name':'HackerTarget', 'value': HackertargetHandler},
        {'id': '12','name':'WaybackMachine', 'value': WaybackmachineHandler},
        {'id': '13','name':'VirusTotal', 'value': VirustotalHandler}
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

    for selected_handler in selected_handlers:
        if selected_handler in handlers_choices:
            for handler in handlers:
                if selected_handler == handler['name']:
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
            
            s = f"\n{'-'*20}[Starting...]{'-'*20}"
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
