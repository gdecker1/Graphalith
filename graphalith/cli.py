"""CLI interface for graphalith project.

Be creative! do whatever you want!

- Install click or typer and create a CLI app
- Use builtin argparse
- Start a web application
- Import things from your .base module
"""
from graphalith.base import*

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m graphalith` and `$ graphalith `.

    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """
        # prompt for input string
    while True:
        try:
            input_string = input("\nEnter an expression string: ")
        except ValueError:
            print("Oops!  That was no valid string.  Try again...")
    
        expression = Expression(value=input_string, auto_format=True, auto_eval=True)
        print(expression)

