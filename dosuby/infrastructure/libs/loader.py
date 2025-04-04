from threading import Thread
from time import sleep
from shutil import get_terminal_size

from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text


class Loader:
    def __init__(self, desc="Loading...", end="\0", timeout=0.1, style="bold green"):
        """
        A loader-like context manager enhanced with Rich styling

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
            style (str, optional): Rich style for the text. Defaults to "bold green".
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.style = style
        self.console = Console()
        
        # Use Rich's built-in spinner formats with styled text
        self.spinner = Spinner("dots", text=Text(desc, style=self.style))
        
        self._thread = Thread(target=self._animate, daemon=True)
        self.done = False
        self._live = None

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        """Animate the spinner using Rich's Live display"""
        with Live(self.spinner, console=self.console, refresh_per_second=10, transient=True) as live:
            self._live = live
            while not self.done:
                live.update(self.spinner)
                sleep(self.timeout)

    def __enter__(self):
        self.start()
        return self

    def stop(self):
        self.done = True
        if self._thread.is_alive():
            self._thread.join(timeout=0.5)
        
        # Clear the line and print the end message
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        
        # Display the end message with [DONE!] appended
        if self.end != "\0":
            # Create a styled text object
            styled_text = Text()
            
            # Add the main message in the specified style
            styled_text.append(self.end, style=self.style)
            
            # Add the [DONE!] text in a bright green style
            styled_text.append(" [DONE!]", style="bold bright_green")
            
            self.console.print(styled_text)
        else:
            self.console.print("Done!", style=self.style)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables
        self.stop()