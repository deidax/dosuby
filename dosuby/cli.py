import sys
import argparse
from dosuby.src.handlers.cli.interruptible_handler import InterruptibleHandler
import inquirer
import re
import sys
from typing import List
import logging
from dosuby.src import *
from art import *
from dosuby.src.utils.helpers import make_interruptible

# Rich imports for better UI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.box import ROUNDED, HEAVY, DOUBLE
from rich.layout import Layout
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.style import Style

# Import version information
try:
    from dosuby.version import __version__ as dosuby_version
except ImportError:
    try:
        from setuptools_scm import get_version
        dosuby_version = get_version(root='..', relative_to=__file__)
    except (ImportError, LookupError):
        dosuby_version = "unknown"

# Create a console instance
console = Console()

def show_version():
    """Display the current version of the dosuby package"""
    console.print(Panel(
        Text(f"Current version: {dosuby_version}", style="bright_white"),
        title="[bold bright_blue]DOSUBY[/bold bright_blue]",
        border_style="bright_blue",
        box=ROUNDED,
        expand=False,
        padding=(1, 2)
    ))
    return 0

def main():
    """Main function for the interactive CLI with enhanced interrupt handling and Rich styling."""
    
    # Set up argument parser for command line options
    parser = argparse.ArgumentParser(description="Dosuby - Subdomain Enumeration and Assessment Tool")
    parser.add_argument('--version', '-v', action='store_true', help='Show the current version and exit')
    
    # Parse arguments
    args, unknown_args = parser.parse_known_args()
    
    # If --version flag is provided, show version and exit
    if args.version:
        return show_version()
    
    try:
        # Initialize interrupt handling at the class level
        InterruptibleHandler.setup_interrupt_handling()
        
        # Display a styled header with app info
        console.print("\n")
        console.print(Panel(
            Text("An Advanced Subdomain Enumeration and Assessment Tool", style="bright_white"),
            title=f"[bold bright_blue]DOSUBY v{dosuby_version}[/bold bright_blue]",
            subtitle="[bright_blue]https://github.com/deidax[/bright_blue]",
            border_style="bright_blue",
            box=DOUBLE,
            expand=False,
            padding=(1, 4)
        ))
        console.print("\n")
        
        # Configure logging with Rich formatting
        logging.basicConfig(
            level=logging.INFO, 
            format="%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Initialize configuration
        config = Config()
        config.scanning_modules = False
        
        # Domain validation regex
        regex = r"^[a-z]{2,}\.[a-z]{2,}$"
        
        # Available handlers with Rich-styled progress indicators
        handlers = [
            {'id': '1', 'name': 'Google', 'value': make_interruptible(GoogleDorkHandler)},
            {'id': '2', 'name': 'Yahoo', 'value': make_interruptible(YahooDorkHandler)},
            # {'id': '3', 'name': 'Duckduckgo', 'value': make_interruptible(DuckduckgoDorkHandler)},
            {'id': '4', 'name': 'Brave', 'value': make_interruptible(BraveDorkHandler)},
            {'id': '5', 'name': 'Aol', 'value': make_interruptible(AolDorkHandler)},
            {'id': '6', 'name': 'Bing', 'value': make_interruptible(BingDorkHandler)},
            {'id': '7', 'name': 'Ask', 'value': make_interruptible(AskDorkHandler)},
            {'id': '8', 'name': 'Crt Search', 'value': make_interruptible(CrtSearchHandler)},
            {'id': '9', 'name': 'Anubis', 'value': make_interruptible(AnubisHandler)},
            {'id': '10', 'name': 'AlientVault', 'value': make_interruptible(AlientvaultHandler)},
            {'id': '11', 'name': 'HackerTarget', 'value': make_interruptible(HackertargetHandler)},
            {'id': '12', 'name': 'WaybackMachine', 'value': make_interruptible(WaybackmachineHandler)},
            {'id': '13', 'name': 'VirusTotal', 'value': make_interruptible(VirustotalHandler)}
        ]

        # Extract handler names for choices
        handlers_choices = [handler['name'] for handler in handlers]
       
        # Define inquirer questions with improved styling
        console.print("[bold bright_blue]Please enter scan parameters:[/bold bright_blue]")
        questions = [
            inquirer.Text(
                'TLD', 
                message="What's the domain to enumerate",
                validate=lambda _, x: re.match(regex, x)
            ),
            inquirer.Checkbox(
                'handlers',
                message="Choose methods to use for the enumeration (Press ENTER for all, SPACE to select specific options)",
                choices=handlers_choices,
            ),
            inquirer.Confirm(
                "scanning_modules", 
                message="Do you want to scan subdomains for vulnerabilities?",
            )
        ]
        
        # Prompt user and collect answers
        answers = inquirer.prompt(questions)
        
        # Check if user cancelled prompt
        if answers is None:
            console.print(Panel(
                "Process cancelled by user",
                title="[bold red]Scan Aborted[/bold red]",
                border_style="red",
                box=ROUNDED
            ))
            return 0
        
        # Extract answers
        target_uri = answers.get('TLD')
        selected_handlers = answers.get('handlers')
        config.scanning_modules = answers.get('scanning_modules')
        
        # Display scan configuration
        config_table = Table(
            title="Scan Configuration",
            box=ROUNDED,
            border_style="bright_blue"
        )
        
        config_table.add_column("Parameter", style="bright_blue")
        config_table.add_column("Value", style="bright_white")
        
        config_table.add_row("Target Domain", f"[bold bright_green]{target_uri}[/bold bright_green]")
        
        if selected_handlers:
            config_table.add_row(
                "Selected Methods", 
                ", ".join(f"[cyan]{h}[/cyan]" for h in selected_handlers)
            )
        else:
            config_table.add_row("Selected Methods", "[cyan]All Available Methods[/cyan]")
            
        config_table.add_row(
            "Vulnerability Scanning", 
            "[bright_green]Enabled[/bright_green]" if config.scanning_modules else "[yellow]Disabled[/yellow]"
        )
        
        console.print(config_table)
        
        # Find selected handlers
        found_handlers: List[dict] = []
        for selected_handler in selected_handlers:
            if selected_handler in handlers_choices:
                for handler in handlers:
                    if selected_handler == handler['name']:
                        found_handlers.append(handler)
        
        # If no handlers selected, use all handlers
        handlers_selected: List = []
        if not found_handlers:
            all_handlers = handlers
            for h in all_handlers:
                handlers_selected.append(h.get('value'))
        
        # Set up handler chain
        handlers_selected_objects: List = []
        
        for handler in found_handlers:
            handler_class_name = handler.get('value')
            handlers_selected.append(handler_class_name)
        
        for handler_selected_class_name in reversed(handlers_selected):
            handler_object = None
            next_handler = None
            if handlers_selected_objects:
                next_selected_handler = handlers_selected_objects[-1]
                next_handler = next_selected_handler
                
            handler_object = handler_selected_class_name(next_handler=next_handler)
            handlers_selected_objects.append(handler_object)
        
        handlers_to_use = handlers_selected_objects[::-1]
        
        # Start the handler chain with a stylish progress indicator
        console.print("\n")
        console.print(Panel(
            Text("Starting subdomain enumeration...", style="bright_white"),
            title="[bold bright_blue]Scan Initiated[/bold bright_blue]",
            border_style="bright_blue",
            box=ROUNDED
        ))
        console.print("\n")
        
        # Execute handlers with built-in interrupt checking
        handler_starter = handlers_to_use[0]
        handler_starter.handle(uri=target_uri)
        
        # Check for interrupt one more time before displaying final results
        InterruptibleHandler.check_for_interrupt()
        
        # Display report with enhanced styling
        console.print("\n")
        console.print(Panel(
            Text("Enumeration Results", style="bright_white"),
            title="[bold bright_blue]Scan Complete[/bold bright_blue]",
            border_style="bright_blue",
            box=ROUNDED
        ))
        
        report = CliReportRepo()
        report.read_report()
        
        # Display completion message
        console.print("\n")
        console.print(Panel(
            Text("All tasks completed successfully. Press Ctrl+C to exit.", style="bright_white"),
            title="[bold bright_green]Scan Summary[/bold bright_green]",
            border_style="bright_green",
            box=ROUNDED
        ))
        
        return 0
            
    except Exception as ex:
        # Handle other exceptions with improved styling
        console.print("\n")
        console.print(Panel(
            Text(f"{str(ex)}", style="bright_white"),
            title="[bold red]Error Occurred[/bold red]",
            border_style="red",
            box=ROUNDED
        ))
        
        # Try to show report even if there was an error
        try:
            console.print("\n")
            console.print(Panel(
                Text("Results collected before error:", style="bright_white"),
                title="[bold yellow]Partial Results[/bold yellow]",
                border_style="yellow",
                box=ROUNDED
            ))
            
            report = CliReportRepo()
            report.read_report()
        except Exception as report_ex:
            console.print(f"[red]Could not display report: {str(report_ex)}[/red]")
                
        return 1

if __name__ == "__main__":
    sys.exit(main())