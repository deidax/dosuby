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
from src.repositories.cli_report_repo import CliReportRepo
from src.handlers.cli.anubis_dork_handler import AnubisHandler
from src.handlers.cli.ask_dork_handler import AskDorkHandler
from src.handlers.cli.alientvault_handler import AlientvaultHandler
from src.handlers.cli.hackertarget_handler import HackertargetHandler
from src.handlers.cli.waybackmachine_handler import WaybackmachineHandler
from src.handlers.cli.virustotal_handler import VirustotalHandler

def main():
    """Main function for the interactive CLI."""
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
    ]
    
    answers = inquirer.prompt(questions)
        
    print(answers.get('handlers'))
    found_handlers = []

    for handler in handlers:
        if handler['name'] in answers.get('handlers'):
            found_handlers.append(handler)

    if found_handlers:
        print("Handlers found:")
        for handler in found_handlers:
            print("Name:", handler['name'])
            print("Value:", handler['value'])
    else:
        print("Handlers not found.")


if __name__ == "__main__":
    main()
